
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

/* 6 */
select propertyid, title, description, datebooked, startdatetime, enddatetime from
property natural join propertybooking
where EXTRACT(DAY FROM propertybooking.startdatetime) <= 10
and EXTRACT(DAY FROM propertybooking.enddatetime) >= 10;

/* 7 */
select employeeid, firstname, lastname, branch.branchid, branch.name as branch_name, salary
from branch left join employee on branch.branchid = employee.branchid
where salary >= 15000.00
order by managerid, employeeid;

/* 9 */
update phonenumber
set phonenumber = '1239872000'
where userid = 466111;

/* 10 */
create function FirstNameFirst(firstName varchar, lastName varchar)
returns varchar as $fullName$
begin
return concat(firstName, ' ', lastName);
end;
$fullName$ language plpgsql;
