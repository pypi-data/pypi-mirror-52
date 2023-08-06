# ============================================================================
# ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.wfadaptations -t test_wfadaptations.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.wfadaptations.testing.COLLECTIVE_WFADAPTATIONS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/collective/wfadaptations/tests/robot/test_wfadaptations.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a manager I want to be able to associate a workflow adaptation
  Given a logged in manager
   When I associate a workflow adaptation
   Then I see parameters form

Scenario: Valid workflow adaptation parameters lead to success message
  Given a logged in manager
   When I associate a workflow adaptation
   And I enter valid parameters
   Then I see success message

Scenario: Invalid workflow adaptation parameters lead to failure message
  Given a logged in manager
   When I associate a workflow adaptation
   And I enter invalid parameters
   Then I see failure message

Scenario: New adaptation is added to adaptations list
  Given a logged in manager
   When I associate a workflow adaptation
   And I enter valid parameters
   Then I see the new adaptation in list

Scenario: Warning message if there is now workflow adaptations
  Given a logged in manager
   When I go to manage adaptations page
   Then I see a warning message

Scenario: As a manager I want to see Manage Workflow Adaptations link in control panel
  Given a logged in manager
   When I go to control panel
   Then I see Manage Workflow Adaptations link

Scenario: I can't apply the same adaptation twice on the same workflow
  Given a logged in manager
    When I associate a workflow adaptation with valid parameters
    And I associate a workflow adaptation with valid parameters
    Then I see failure message


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------


# --- WHEN / AND --------------------------------------------------------------

I go to manage adaptations page
  Go to  ${PLONE_URL}/@@manage_workflow_adaptations

I associate a workflow adaptation
  I go to manage adaptations page
  Select from list  form.widgets.adaptation:list  collective.wfadaptations.example
  Select from list  form.widgets.workflow:list  intranet_workflow
  Click Button  Next

I enter valid parameters
  Input text  form.widgets.state_name  internal
  Input text  form.widgets.new_state_title  New title
  Click Button  Save

I enter invalid parameters
  Input text  form.widgets.state_name  foobar
  Input text  form.widgets.new_state_title  Internal draft
  Click Button  Save

I go to control panel
  Go to  ${PLONE_URL}/@@overview-controlpanel

I associate a workflow adaptation with valid parameters
  I associate a workflow adaptation
  I enter valid parameters

# --- THEN -------------------------------------------------------------------

I see parameters form
  Wait until page contains  Site Map
  Page should contain  Choose parameters for your workflow adaptation
  Page should contain element  form.widgets.state_name
  Page should contain element  form.widgets.new_state_title

I see success message
  Wait until page contains  Site Map
  Page should contain  The workflow adaptation has been successfully applied.

I see failure message
  Wait until page contains  Site Map
  Page should contain  The workflow adaptation has not been successfully applied.

I see the new adaptation in list
  Wait until page contains  Site Map
  Page should contain element  applied-adaptations
  Page should contain  intranet_workflow
  Page should contain  intranet_workflow
  Page should contain  internal
  Page should contain  New title

I see a warning message
  Wait until page contains  Site Map
  Page should not contain  applied-adaptations
  Page should contain  There is no applied workflow adaptations for now

I see Manage Workflow Adaptations link
  Wait until page contains  Site Map
  Page should contain link  css=a[href$=manage_workflow_adaptations]
