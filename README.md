Database Search

Introduction:
Database Search is a web application developed using Flask, a Python web framework, designed to facilitate searching and browsing of a database of items. It allows users to search for items by code number or description and provides search results with relevant information.

Features:

    User Authentication: Users can register, log in, and log out securely.
    Database Search: Users can search for items in the database by code number or description.
    Auto-completion: The search input fields provide auto-completion suggestions based on the user's input.
    Responsive Design: The frontend of the application is designed to be responsive, providing optimal viewing and interaction experience across a wide range of devices and screen sizes.
    Session Management: User sessions have an expiration time, and users are automatically logged out after a period of inactivity.
    User Role Change: If a user's role or permissions are changed while they are logged in, they are automatically logged out to ensure they only have access to appropriate resources.
    Account Deactivation: If a user's account is deactivated or deleted, they are logged out immediately to prevent further access.
    IP Address Change: If the user's IP address changes unexpectedly during a session, they are logged out to mitigate potential security threats.

Technologies Used:

    Flask: Python web framework used for backend development.
    SQLite: Lightweight relational database management system used for storing user data and database items.
    SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python used for database management.
    HTML/CSS: Frontend markup and styling languages used for building user interfaces.
    JavaScript/jQuery: Client-side scripting language and library used for dynamic interactions and auto-completion functionality.

Installation and Setup:

    Clone the repository from GitHub.
    Install Python and the required dependencies using pip.
    Run the Flask application using the flask run command.
    Access the application through a web browser at the specified URL.

Usage:

    Register a new account or log in with existing credentials.
    Search for items in the database using code numbers or descriptions.
    View search results and navigate through the application.
    Log out when done to securely end the session.

Future Enhancements:

    Implement additional features such as pagination for search results.
    Improve the user interface with modern design elements and animations.
    Add functionality for users to edit and update their account information.
    Enhance security measures, such as implementing HTTPS and CSRF protection.
    Scale the application to handle larger datasets and more concurrent users.

Contributors:

    Usmonjov M
