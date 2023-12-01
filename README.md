# Email-editor with FastAPI

## Overview

This small-scale project emerged from operational needs encountered during the development of a larger project in my professional capacity. The primary goal was to address the operational team's requirement for mass customization of outbound communications without impeding the progress of the larger project.

## Technologies Used

- Frontend: Vue.js
- Backend: FastAPI
- Database: MongoDB

## Background

Given the uncertainty surrounding the content provided by existing websites offering similar functionalities and the desire to avoid incurring additional expenses (typically involving a fixed fee), I dedicated approximately 1-2 days of my spare time to developing a simple single-page website using an existing open-source library (vue-email-editor).

## Functionality

The website, powered by Vue.js, facilitates the mass dispatch of customized communications. It reads the content for outbound communications from a table and stores it in MongoDB through the FastAPI backend. Subsequently, the customized content is replaced, and a large volume of emails are sent using Google SMTP.

## Decision Making

The decision to opt for open-source software (vue-email-editor) and the Vue.js framework was influenced by the desire to balance functionality with avoiding unnecessary costs. FastAPI was chosen for the backend to ensure efficient handling of data between the frontend and the MongoDB database.

## Docker-Compose Integration

To simplify deployment and local testing, this project utilizes Docker-Compose to automatically run the frontend, backend, and database locally. The Docker configuration is provided in the repository for easy setup.

## Conclusion

Although the operational team eventually opted to allocate budget for a formal outbound communication platform, this project was not intended for ongoing operation or updates. Nevertheless, the integration and development process proved to be an engaging and insightful experience.

## Usage

To use this project:

1. Clone the repository.
2. Install dependencies with `npm install`.
3. Configure MongoDB and Google SMTP settings.
4. Run the application using `docker-compose up`.
5. Access the website and customize mass communications as needed.

**Please note that this project is not actively maintained, and users are encouraged to explore more robust solutions for long-term operational use.**