Exercises to complete on the simple load database (SQLite):

1. Write a query that returns the count of each `customer_type`
2. Write a query that returns the total value of loans per `customer_type`
3. Write a query that returns which businesses have at least two directors
4. Write a query that returns the total value of loans per business. If the business does not have a loan, show 0 for that business
5. Write a query that returns which businesses have both at least one director and belong to a lending group
6. Write a query that returns all the children of the `LEN559852` lending group
7. Write a query that returns all the children and grandchildren of the `LEN559852` lending group
8. Write a query that returns all the descendants of the `LEN559852` lending group
9. Write a query that returns all the customers related to the `IND154203` individual. This should include relatives of all depths and generations
10. Write a query to identify how many distinct family trees belong in the database
11. Define the total relative capital for a customer to be the sum of their loans' values, plus the sum of the loan values for all of their descendents. Write a query that returns the customer with the highest total relative capital
12. Repeat Q11 but exclude the `LEN559852` lending group
