---
unit: auth/password-reset
version: 0.1.0
status: draft
author: nevada.hamaker
exposes:
  - POST /auth/password-reset/request
  - POST /auth/password-reset/redeem
depends_on:
  - auth/password-policy
  - auth/session
  - notifications/email-dispatch
must_not_know:
  - auth/oauth
  - auth/magic-link
  - user/profile
---

# Intent: Password Reset Flow

## Summary

Allow a user who cannot log in to regain access by requesting a time-limited, single-use reset token delivered via email. The system must not reveal whether an email address has an account.

---

## Domain Semantics

**Reset token** — A cryptographically random, opaque string generated at request time. It is not a password, not a session credential, and carries no user identity in its structure. Its only meaning is: "someone with access to this email address asked to reset their password at a specific point in time."

**Token window** — The period during which a token can be redeemed. Expiry is measured from generation time, not from email delivery. If delivery is delayed, the window still closes at the same wall-clock time.

**Account enumeration** — An attack where an attacker determines whether a given email address has a registered account by observing different system responses. This flow must not enable enumeration: the response to a reset request must be identical whether or not the email exists.

**Redemption** — The act of submitting a valid token and a new password. Successful redemption invalidates the token and updates the credential. It does not log the user in.

---

## Behavioral Contract

### Preconditions

- The requesting client has access to a valid email address (no verification required by this unit — that is the caller's concern).
- The email service dependency is reachable (see `depends_on`).
- Password policy rules are available to validate the new password (see `depends_on`).

### Postconditions

**On successful request (email exists):**
- A reset token is persisted, associated with the account, with a generation timestamp.
- Any previously issued, unused tokens for that account are invalidated.
- An email containing the token (or a link embedding the token) is dispatched to the address.
- The API response is identical to the "email not found" case.

**On successful request (email does not exist):**
- No token is created.
- No email is sent.
- The API response is identical to the "email found" case.

**On successful redemption:**
- The account's password credential is replaced with a hash of the submitted password.
- The token is invalidated and cannot be reused.
- All active sessions for the account are invalidated.
- The user is not automatically authenticated.

**On failed redemption (invalid or expired token):**
- The password credential is unchanged.
- The token is not consumed (expired tokens remain expired; invalid tokens remain invalid).
- The response does not distinguish between "token not found", "token expired", and "token already used".

### Invariants

- At most one valid (unexpired, unused) reset token exists per account at any time.
- A token's expiry window is exactly 60 minutes from generation. This is not configurable per-request.
- Tokens are never logged, never included in server-side analytics events, and never appear in URLs in a context where they could be captured by referrer headers.
- The generation timestamp and expiry are stored server-side; the client is not trusted to supply or extend them.

### Scenarios

```gherkin
Feature: Password Reset Flow

  Scenario: Happy path
    Given a registered account with email "user@example.com"
    When a reset is requested for "user@example.com"
    Then a token is generated and persisted
    And the token is dispatched to "user@example.com"
    And the response indicates the request was received

  Scenario: Unknown email
    Given no account exists for "unknown@example.com"
    When a reset is requested for "unknown@example.com"
    Then no token is generated
    And no email is sent
    And the response is identical to the happy path response

  Scenario: Second request before first token used
    Given a token was issued for an account 10 minutes ago and not yet redeemed
    When a second reset is requested for the same account
    Then a new token is generated
    And the previous token is invalidated
    And the new token is dispatched

  Scenario: Redemption within window
    Given a token issued 45 minutes ago
    When it is submitted with a new password that passes policy validation
    Then the account password is updated
    And the token is consumed and cannot be reused
    And all active sessions for the account are invalidated
    And the user is not authenticated

  Scenario: Redemption after expiry
    Given a token issued 61 minutes ago
    When it is submitted with a valid new password
    Then the password is unchanged
    And the response does not distinguish expiry from invalidity

  Scenario: Reuse of a consumed token
    Given a token that was successfully redeemed
    When it is submitted again
    Then the request fails identically to the expired token case

  Scenario: Invalid new password
    Given a valid unexpired token
    When it is submitted with a password that fails policy validation
    Then the password is unchanged
    And the token is not consumed
    And the validation error is returned

  Scenario: Email delivery failure
    Given a registered account
    And the email service is reachable but failing
    When a reset is requested
    Then no token is persisted
    And the caller receives a 503 error
```

---

## Quality Attributes

```yaml
security:
  token_entropy_bits: 128
  token_source: cryptographically_secure_random
  token_comparison: constant_time
  rate_limits:
    per_email:
      requests: 3
      window_minutes: 15
    per_ip:
      requests: 10
      window_minutes: 15
  rate_limit_response: must_not_reveal_which_limit_hit

performance:
  request_endpoint_p99_ms: 500
  request_email_dispatch: async
  redemption_endpoint_p99_ms: 300

failure_modes:
  token_store_unavailable: return_503_no_token_generated
  email_service_unavailable: return_503_no_token_persisted
  password_policy_unavailable_at_redemption: return_503_no_credential_update
```

---

## Rationale

**60-minute expiry, not 15 or 24 hours**
15 minutes creates support burden — users who don't check email promptly face friction. 24 hours creates an unacceptably wide window where a compromised inbox can be exploited without the account owner noticing. 60 minutes balances usability against exposure.

**No automatic login after redemption**
Automatically logging in after reset conflates credential recovery with session establishment. It also creates a vector where anyone with brief inbox access can establish a session that persists beyond the reset window. Requiring explicit login after reset keeps the flows cleanly separated.

**Atomic token-or-error on email failure**
Persisting a token that was never delivered creates a phantom: the token exists in the store but the user has no way to retrieve it. The next request will invalidate it, but in the window between, support requests are unanswerable. Atomic behavior eliminates this state entirely.

**Magic links considered and rejected**
A pure magic link (clicked link logs user in directly) conflates reset with authentication, creates session-from-inbox access, and is harder to scope correctly. Token-in-link (link opens a form, user submits token + new password) keeps reset as credential replacement only.

**One valid token per account**
Allowing multiple valid tokens widens the window for inbox-compromise attacks and creates ambiguity about which request was most recent. Invalidating prior tokens on new request is a minor UX cost with a clear security benefit.
