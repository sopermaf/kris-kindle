# Kris Kindle - Secret Santa

This is a simple project to run the setup for Kris Kindle.

Using only py38+ standard library

This requires the input of a list of names and emails of the participants
and also an email account to send the emails containing each users secret person.


# HOW TO RUN

1. configure `users.csv` as per the example file `users.example.csv`
2. setup env vars for running. see `.env.example` for required vars
    - default setup is using gmail smtp setup
        -> may require enabling non-secure apps for google account
