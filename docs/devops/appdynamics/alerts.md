
---
layout: default
title: Alerts
parent:  AppDynamics
grand_parent: DevOps
nav_order: 2
---



To create an alert in AppDynamics, you first need to set up health rules and then configure policies to trigger actions like sending notifications. Follow these steps:

## Step 1: Create a Health Rule
Health rules define the conditions under which alerts should be triggered.

3. **Click "Create Health Rule"**.
5. Choose the **affected entity type** (e.g., a specific node, tier, or application).
6. **Set Conditions**:
   - Define the metrics (e.g., CPU usage, memory, response time) and threshold values for critical or warning conditions.
7. Optionally, you can configure **multiple conditions** using logical operators (AND/OR).


## Step 2: Configure a Policy to Trigger Alerts

Now, associate the health rule with actions like sending notifications when a violation occurs.

1. Go to the **Alert & Respond** section and click on **Policies**.
2. **Click "Create a Policy"**.
3. Enter a name and description for the policy.
4. In the **Policy Trigger** section, select **Health Rule Violation**.
5. Select the **Health Rule** you created earlier.
6. In the **Actions** section, define what happens when the rule is violated:
   - **Send Email**: Add email recipients.
   - **SMS**: Configure to send a text message.
   - **Integration**: Use services like Slack, PagerDuty, or webhooks to notify your team.

