## welcome
* hello
  - utter_welcome
  - utter_registrate_info
  - utter_passreset_info
  - action_restart

## create user happy path
* create_user
  - utter_create_confirm
* positive
  - utter_wait
  - action_create_user
  - utter_invitation
  - action_invite_user
  - action_restart

## create user sad path 
* create_user
  - utter_create_confirm
* negative
  - utter_refuse
  - action_restart

## reset password happy path
* reset_password
    - utter_reset_confirm
* positive
    - utter_wait_reseting
    - action_reset_password
    - action_restart

## reset password sad path
* reset_password
    - utter_reset_confirm
* negative
    - utter_refuse
    - action_restart

## fallback
- custom_fallback_action