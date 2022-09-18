# Gmail Scrapping

## Scrapping Bank Transaction Alert for Monthly Analysis 

Everytime a transaction is carried out with my bank account, a mail is sent to my Gmail. This mail comes with a transaction summary which includes account number, account name, description, reference number, transaction branch, transaction date, value date and available balance. As an individual, I would love to view my whole transaction details from a dashboard, for instance, through Microsoft Power BI mobile app. 

The aim of this project is to use the gmail api to access and extract few parameters from the transaction summary, then save it as a file. This file will then be used for visualization on Microsoft Power BI.

## Modules Used
> Gmail API
>
> Base64
>
> BeautifulSoup
>
> Regular Expression 
>
> Pandas

## Summary Of Function
I wrote a function that has three parameters, maximum result, convert to excel and convert to csv. Whhen called, the function produce a dataframe of transactions corresponding to the given argument. Below is the definition and body contents of the function.

* `maxResult`: This denotes the number of transaction to be extracted. Default is 50.
* `excel`: This parameter accept bool. When set to `True`, it wil create an excel file of the extracted transactions. Default is `False`
* `csv`: This is similar to excel. This parameter when set to `True` will create a csv file in the working directory. Default is `False` 
* A `filter` variable that holds the filtered message and thread IDs.
* `id_lst` which holds the appended message ids from the previous step.
* A loop which iterate over the available message ids and do the following:
    * extract the `amount` and `a/c number` from the message snippet.
    * extract the `datetime` from the message payload headers.
    * then extract the `description`, `reference number` and `transaction branch` from the data section of the message body.
* Check what type of transaction it was, `Credit` or `Debit`
* Append the above information to a dictionary.
* Returned the information back as a dataframe when the function is called.

## Summary Of EDA