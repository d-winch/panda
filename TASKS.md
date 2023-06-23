# Task List

* ~~It should be possible to add patients to and remove them from the PANDA.~~
* ~~It should be possible to check~~ ~~and update patient details in the PANDA.~~
* ~~It should be possible to add new appointments to the PANDA~~, ~~and check and update appointment details~~.
* The PANDA may need to be restarted for maintenance, and the data should be persisted.
* ~~The PANDA backend should communicate with the frontend via some sort of HTTP API.~~
* ~~The PANDA API does not need to handle authentication because it is used within a trusted environment.~~
* Errors should be reported to the user. ~ *Given more time, abstract and add structure to errors, add more specific errors, pass back the request...*

There are some additional requirements for the data:

* ~~Appointments can be cancelled~~~~, but cancelled appointments cannot be reinstated.~~ ~ N.B., I have disallowed editing
* Appointments should be considered 'missed' if they are not set to 'attended' by the end of the appointment. ~ If forgotten to do so, could lead to incorrect statistics. Generate field based on attended_at
* ~~Ensure that all [NHS numbers are checksum validated](https://www.datadictionary.nhs.uk/attributes/nhs_number.html).~~
* Ensure that all [postcodes can be coerced into the correct format](https://ideal-postcodes.co.uk/guides/uk-postcode-format).


**A separate team has been tasked with building the frontend for the application.** You've spoken with this team to iron out the separation of responsibilities:

* They're quite flexible about what they can build, and willing to defer to your choices about implementation.
* They're flexible about how they interact with the API, as long as you can provide guidance and they can get data in JSON format.
* Due to time constraints, they will not be able to properly validate the inbound data in the frontend, but can propagate error responses returned by the backend.
* All timestamp passed between the backend and frontend must be timezone-aware.


## Additional Considerations

As you've worked with the client for a while, you have an awareness of some past issues and upcoming work that it might be worth taking into consideration:

* The client has been burned by vendor lock-in in the past, and prefers working with smaller frameworks.
* The client highly values automated tests, particularly those which ensure their business logic is implemented correctly.
* The client is in negotiation with several database vendors, and is interested in being database-agnostic if possible.
* The client is somewhat concerned that missed appointments waste significant amounts of clinicians' time, and is interested in tracking the impact this has over time on a per-clinician and per-department basis.
* The PANDA currently doesn't contain much data about clinicians, but will eventually track data about the specific organisations they currently work for and where they work from.
* The client is interested in branching out into foreign markets, it would be useful if error messages could be localised.
* The client would like to ensure that [patient names can be represented correctly, in line with GDPR](https://shkspr.mobi/blog/2021/10/ebcdic-is-incompatible-with-gdpr/).
