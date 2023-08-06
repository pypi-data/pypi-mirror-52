=========================================
Requirements Trace Matrix (RTM) Validator
=========================================

Validate a Function & Design Requirements document.

Free software: MIT license


J&J Quick Start
---------------
1. **Install Python**
    a. Navigate to J&J App Store. You may need to use Internet Explorer. Users have had difficulty with Chrome.
    #. Search ``Python``. You should see something similar to ``Python 3.6``. Add it to cart and install.
    #. No restart is required.
#. **Run Command Prompt with Elevated Privileges**
    a. Do not call IRIS.
    #. Hit the ``Windows Key`` and type ``cmd`` to search for the Windows command prompt
    #. Right-click ``cmd`` and select ``open file location``. This opens File Explorer.
    #. Right-click on the ``cmd`` icon and select ``Run with elevated privileges``.
#. **Install** ``dps-rtm``
    a. In Command Prompt, type ``pip install dps-rtm``
    #. If this throws an error, try instead: ``python -m pip install dps-rtm``. Hint: the up-arrow accesses previous commands to reduce the amount of typing you need to do.
    #. Note: You might see a note about ``pip`` being out of date. This is ok, but feel free to update it as suggested.
#. **Run** ``rtm``
    a. In Command Prompt, type ``rtm``

Validation Rules
-----------------
General Notes
'''''''''''''
- The FDR sheet must have the title 'Procedure Based Requirements'
- If multiples headers share the same name, only the first will be used.
- All columns get checked for 1) Exist and 2) Correct left-to-right order.

ID
''

- Each ID must be unique (done!)
- sorts alphabetically (done!)
- Procedure Step IDs must be formatted "PXYZ" e.g. "P010" (done!)
- All other IDs must start with the ID of its root Procedure Step. Example: if a Procedure Step has an ID of "P010", then the following VOC USER NEED could have an ID of "P010-0010". (done!)

Cascade Block
'''''''''''''
- must contain at a minimum these columns:
    - Procedure Step
    - Need
    - Design Input
    - Solution Level 1
- optionally, may also contain these columns:
    - Solution Level 2
    - Solution Level 3
    - ...
    - Solution Level n
- one and only one cell gets marked
- no missing steps
- each requirements path starts with Procedure Step
- each requirements path terminates in 'F' (done)
- all DO Solution levels get used (done)
- only contains characters X or F (done)

Cascade Level
'''''''''''''
- NOT EMPTY (done!)
- VALID ENTRIES: is "procedure step", "voc user need", "business need", "risk need", "design input", or "design output solution" (done!)
- MATCHING LEVEL: matches selection in Cascade Block (done!)

Requirement Statement
'''''''''''''''''''''
- Not empty (WorkItemObject)
- CHILD - valid pointer
- ADDITIONALPARENT 
- valid pointer (CascadeObject)
- check for ______ hashtags e.g. #Function, #MatingParts
- report on extra tags found?

Requirement Rationale
'''''''''''''''''''''
- not empty (done)

VorV Strategy
'''''''''''''
- not empty (done)
- if "business need", strategy is not required. Use N/A (is this true?)

VorV Results
''''''''''''
- not empty
- if "business need", results are not required. all others require results (Use 'N/A' in this cell?)
- if windchill number is present, check its formatting. (10 digits)
- print report of applicable documents? (?)

Devices
'''''''
- not empty
- no repeats in cell
- print report of device list?

DO Features
'''''''''''
- not empty
- if contains features that are CTQs, CTQ ID should be formatted as "(CTQ##)"
- if contains features that are CTQs, check that CTQ Y/N column is "yes"
- print report of CTQ IDs and correlated features/devices?

CTQ Y/N
'''''''
- not empty
- validated input list
- is "yes", "no", "N/A", or " - " (only procedure step can have " - ")
- if yes, check for CTQ IDs in DO Features column

Other
'''''
- 'N/A' check? (WorkItemObject)
- " - " check

Developer Notes
---------------
How It Works
''''''''''''''
The Requirements Trace Matrix (RTM) documents the requirements cascade for an New Product Development (NPD) project.
Broad core requirements flow into multiple subrequirements, which themselves spawn yet more subrequirements, and so on.
Each (sub)requirement can have multiple parents, though most have only one.
Each of these (sub)requirements is called a **work item**.

Expressed in terms of `Graph Theory <https://en.wikipedia.org/wiki/Graph_theory>`_,
the RTM is a collection of one or more directed, acyclic graphs.
Each graph node is represented as a single row in the RTM Excel worksheet.
Each node has multiple fields, represented by worksheet columns.
The graph edges are represented by the worksheet's Cascade Block. To find a node's primary parent,
find the last '**X**' in the previous column of the Cascade Block.
All other parents are called out with tags in the **Requirements Statement** field.

The RTM Validator works by first reading all rows of each field into an object.
Then each work item (node) is read into its own object.
Finally, validation functions are called, field by field.
The output (pass/warning/fail) is displayed on the console.


Release History
---------------

v 0.1.1
''''''''''
* Initial PyPI upload

v 0.1.2
''''''''''
* added README

v 0.1.3|4|5
''''''''''''
* implement tkinter

v 0.1.6
''''''''''
* implement click cli

...

v 0.1.16
''''''''''''
* add Cascade Block validation

v 0.1.17
''''''''''''
* add Cascade Level validation
