# Initial Thoughts

## Key Points

- The app is to be an MVP to replace an ageing system.
- It needs to implement the current system functionality
- Additional functionality will be added when it's live.
- It is used internally and there is no need to authentication at this stage.
- Requires automated tests - particularly those which ensure their business logic is implemented correctly. BDD
- "The client has been burned by vendor lock-in in the past, and prefers working with smaller frameworks."
- "The client is interested in branching out into foreign markets, it would be useful if error messages could be localised."
- "The client would like to ensure that patient names can be represented correctly, in line with GDPR."

&nbsp;

## Framework Choice

Django REST is a full-stack framework and may cause vendor lock-in, a lot of configuration, etc. It also does not allow much flexibility compared to other frameworks due to its opinionated ways.

Flask is a lightweight micro-framework but can require a lot of time to build an MVP from scratch. It is single threaded and not asynchronous by default. It can be vulnerable to security issues depending on a developer's implementations. If building an MVP in the time restraints, problems could be introduced.

FastAPI is a micro-framework with a lot of quality-of-life functionality. Unlike Flask, it has numerous built in concepts to make development quicker and easier. These concepts are extendable and allow for customised paradigms. FastAPI will handle a lot of our error checking and produces specific errors such as when a required field is missing which makes our job a lot easier! FastAPI also produces an OpenAPI documentation automatically. This documentation can be customised through our code, which also helps the code to be self-documenting.

FastAPI implements/extends Starlette and Pydantic models. The application could be moved over to another framework and continue to use these.

&nbsp;

## Resources and Nouns

Patients

- Get
- Post
- Put
- Delete

Appointments

- Get
- Post
- Put

Others (for functionality/future) -

Clinicians

Departments

Organisations

Departments
