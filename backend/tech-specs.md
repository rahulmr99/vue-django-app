# Architectural Overview

## SMS Bot architecture

mobile <-> SMS <-> twilio API <-> AWS API Gateway <-> backend-zappa-lambda stack <-> lex

https://aws.amazon.com/blogs/machine-learning/integrate-your-amazon-lex-bot-with-any-messaging-service/

## REST APIs

Browser <-> API Gateway <-> Zappa handler <-> django router/view <-> RDS


# Database Schema

When a user signs up from [admin_panel](app.bookedfusion.com) 
1. we create a `appsettings.generalsettings` which represents a company
2. a provider account with created with root_user attribute checked in.

Each `appsettings.generalsetting` 
    -> represents a company
        -> each one has many Admins/Providers/Customers
            -> Admins/Providers can login to admin_panel and see their appointments
            -> Customer accounts created when new appointments created with any of the provider of that company.
    -> Data/Customer of one company should not be visible to other. 
        -> to do this each API requires the `company_id/generalsettings_id` in the request 
           and the data is filtered accordingly.
