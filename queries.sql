
/* 3 */
select bookingid, propertyid,userid,numguests,datebooked,startdatetime,enddatetime,price from
propertybooking natural join propertypayments, payment
where propertypayments.paymentid = payment.paymentid and payment.status = 'completed'
order by propertybooking,price
limit 1;

/* 4 */
with s as (
select propertyid, avg(rating) as review_rating from
propertyreview
group by propertyid
)
select propertyid, title, description, branchid, review_rating from
property natural join s
order by branchid, review_rating;

/* 5 */
select distinct propertyid, hostid, branchid, title, description, numguests, numbedrooms, numbaths, numbeds from
property except
(
	select propertyid, hostid, branchid, title, description, numguests, numbedrooms, numbaths, numbeds from
	property natural join propertybooking
);

/* 10 */
create function FirstNameFirst(firstName varchar, lastName varchar)
returns varchar as $fullName$
begin
return concat(firstName, ' ', lastName);
end;
$fullName$ language plpgsql;
