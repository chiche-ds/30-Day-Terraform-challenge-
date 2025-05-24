#!/usr/bin/env python3
import os
from datetime import datetime, timedelta
from github import Github
import pytz

# Initialize GitHub client
g = Github(os.environ['GITHUB_TOKEN'])
repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])

def get_week_number():
    start_date = datetime(2025, 5, 26)  # Challenge start date
    today = datetime.now()
    delta = today - start_date
    return (delta.days // 7) + 1

def get_current_focus():
    week = get_week_number()
    focus_areas = {
        1: "Fundamentals - IaC Concepts & Terraform Basics",
        2: "Resource Management - Variables, Dependencies & State",
        3: "Advanced Concepts - Remote State & Workspaces",
        4: "Certification Prep - Best Practices & Mock Exams"
    }
    return focus_areas.get(week, "Challenge Complete")

def get_next_checkin_date():
    # Get next Friday
    today = datetime.now()
    days_until_friday = (4 - today.weekday()) % 7
    next_friday = today + timedelta(days=days_until_friday)
    return next_friday.strftime('%Y-%m-%d')

def create_weekly_reminder():
    week_number = get_week_number()
    if week_number > 4:
        return  # Challenge is over
        
    next_checkin = get_next_checkin_date()
    focus = get_current_focus()
    
    # Read template
    with open('.github/REMINDER_TEMPLATES/check-in-reminder.md', 'r') as f:
        template = f.read()
    
    # Customize template
    reminder = template.replace('[DATE]', next_checkin)
    reminder = reminder.replace('[WEEK_NUMBER]', str(week_number))
    reminder = reminder.replace('[FOCUS_AREAS]', focus)
    
    # Create issue
    issue_title = f"Week {week_number} Check-in Reminder - {next_checkin}"
    repo.create_issue(
        title=issue_title,
        body=reminder,
        labels=['reminder', 'check-in']
    )

def create_blog_reminder():
    week_number = get_week_number()
    if week_number > 4:
        return  # Challenge is over
        
    # Calculate blog due date (Sunday)
    today = datetime.now()
    days_until_sunday = (6 - today.weekday()) % 7
    due_date = today + timedelta(days=days_until_sunday)
    
    # Read template
    with open('.github/REMINDER_TEMPLATES/blog-post-reminder.md', 'r') as f:
        template = f.read()
    
    # Customize template
    reminder = template.replace('[DATE]', due_date.strftime('%Y-%m-%d'))
    
    # Create issue
    issue_title = f"Week {week_number} Blog Post Reminder - Due {due_date.strftime('%Y-%m-%d')}"
    repo.create_issue(
        title=issue_title,
        body=reminder,
        labels=['reminder', 'blog-post']
    )

def create_daily_task_reminder():
    # Calculate day number
    start_date = datetime(2025, 5, 26)  # Challenge start date
    today = datetime.now()
    delta = today - start_date
    day_number = delta.days + 1
    
    if day_number > 30:
        return  # Challenge is over
    
    # Read template
    with open('.github/REMINDER_TEMPLATES/daily-task-reminder.md', 'r') as f:
        template = f.read()
    
    # Get topic from milestones
    with open('MILESTONES.md', 'r') as f:
        milestones = f.read()
        # Extract topic based on day_number (simplified)
        topic = get_current_focus()
    
    # Customize template
    reminder = template.replace('[NUMBER]', str(day_number))
    reminder = reminder.replace('[TOPIC]', topic)
    
    # Create issue
    issue_title = f"Day {day_number} Task Reminder"
    repo.create_issue(
        title=issue_title,
        body=reminder,
        labels=['reminder', 'daily-task']
    )

if __name__ == '__main__':
    # Create all types of reminders
    create_weekly_reminder()
    create_blog_reminder()
    create_daily_task_reminder() 