# Gmail Scrapping

## Scrapping Bank Transaction Alert for Monthly Analysis 

Everytime a transaction is carried out on my bank account, a mail is sent to my Gmail. This mail comes with a transaction summary which includes A/C number, account name, description, reference number, transaction branch, transaction date, value date and available balance. As an individual, I would love to view my whole transaction details from a dashboard, for instance, through Microsoft Power BI mobile app. 

The aim of this project is to use the gmail api to access and extract few parameters from the transaction summary, then save it as an excel file. This file will then be used for visualization on Microsoft Power BI.

## Modules Used
> Gmail API
>
> Base64
>
>BeautifulSoup
>
> Regular Expression 
>
> Pandas

## Summary
I wrote a function that takes in a single argument, maximum result, and when called produce a dataframe of transactions corresponding to the given argument. Below is the definition and body contents of the function.

* The function has one parameter, `maxResult`, this specify the total number of transaction I want to retrieve. the default is 50.
* A `filter` variable that holds the filtered message and thread IDs.
* `id_lst` which holds the appended message ids from the previous step.
* A loop which iterate over the available message ids and do the following:
    * extract the `amount` and `a/c number` from the message snippet.
    * extract the `datetime` from the message payload headers.
    * then extract the `description`, `reference number` and `transaction branch` from the data section of the message body.
* Check what type of transaction it was, `Credit` or `Debit`
* Append the above information to a dictionary.
* Returned the information back as a dataframe when the function is called.