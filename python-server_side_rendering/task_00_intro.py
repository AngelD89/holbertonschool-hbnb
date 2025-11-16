#!/usr/bin/python3
"""
Task 0: Creating a Simple Templating Program
This module contains a function to generate personalized invitation files
from a template with placeholders and a list of attendees.
"""


def generate_invitations(template, attendees):
    """
    Generate personalized invitation files from a template and attendees list.

    Args:
        template (str): Template string with placeholders
        attendees (list): List of dictionaries containing attendee information

    Returns:
        None: Writes output files or logs error messages
    """
    # Check input types
    if not isinstance(template, str):
        print("Error: Template must be a string")
        return

    if not isinstance(attendees, list):
        print("Error: Attendees must be a list of dictionaries")
        return

    # Verify attendees is a list of dictionaries
    for attendee in attendees:
        if not isinstance(attendee, dict):
            print("Error: Attendees must be a list of dictionaries")
            return

    # Handle empty template
    if not template or template.strip() == "":
        print("Template is empty, no output files generated.")
        return

    # Handle empty attendees list
    if len(attendees) == 0:
        print("No data provided, no output files generated.")
        return

    # Process each attendee
    for index, attendee in enumerate(attendees, start=1):
        # Create a copy of the template for this attendee
        personalized_invitation = template

        # Replace placeholders with values or "N/A" if missing
        # Extract all placeholders from template
        import re
        placeholders = re.findall(r'\{(\w+)\}', template)

        for placeholder in placeholders:
            value = attendee.get(placeholder)
            # Convert None or missing values to "N/A"
            if value is None or value == "":
                value = "N/A"
            personalized_invitation = personalized_invitation.replace(
                f"{{{placeholder}}}", str(value)
            )

        # Write to output file
        output_filename = f"output_{index}.txt"
        with open(output_filename, 'w') as output_file:
            output_file.write(personalized_invitation)
