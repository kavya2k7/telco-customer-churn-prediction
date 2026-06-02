select * from CustomerChurn

EXEC sp_help CustomerChurn;


--overall churn rate

select count(*) as TotalCustomers,sum(case when Churn = 'Yes' then 1 else 0 end)as ChurnedCustomers,
round (100.0* sum (case when Churn = 'Yes' then 1 else 0 end)/count(*), 2) as ChurnRate_Percent from CustomerChurn;

--CHRUN BY CONTRACT TYPE

select Contract ,count(*) as total,sum(case when Churn = 'Yes' then 1 else 0 end) as Churned,
round(100.0* sum(case when Churn='Yes' then 1 else 0 end)/count(*),2) as ChurnRate from CustomerChurn
group by Contract
order by ChurnRate desc;

--tenure based segmentation

select case 
when Tenure<=12 then 'New (0-12 months)'
when Tenure<=36 then 'Mid (13-36 months)'
else 'Loyal (37+ months)'
end as TenureGroup,
count(*) as total,
sum(case when Churn = 'Yes' then 1 else 0 end) as Churned,
round(100.0* sum(case when churn ='Yes' then 1 else 0 end)/count(*),2) as ChurnRate from customerChurn
group by case
when Tenure<=12 then 'New (0-12 months)'
when Tenure<=36 then 'Mid (13-36 months)'
else 'Loyal (37+ months)'
end 
order by ChurnRate desc;


--high risk customer identification
select CustomerID,Tenure,Contract,MonthlyCharges,TotalCharges from CustomerChurn
where contract='Month-to-month'
and Tenure<12
and MonthlyCharges>70
and Churn='No'
order by MonthlyCharges desc;

--revenue at  risk
select sum(MonthlyCharges) as Monthly_Revenue_lost,sum(TotalCharges) as Total_revenue_lost
from CustomerChurn
where Churn='yes';


--null
SELECT 
    SUM(CASE WHEN CustomerID IS NULL THEN 1 ELSE 0 END) AS Customer_ID_Null_Count,
    SUM(CASE WHEN Gender IS NULL THEN 1 ELSE 0 END) AS Gender_Null_Count,
    SUM(CASE WHEN Partner IS NULL THEN 1 ELSE 0 END) AS partner_Null_Count,
    SUM(CASE WHEN SeniorCitizen IS NULL THEN 1 ELSE 0 END) AS seniorcitizen_Null_Count,
    SUM(CASE WHEN Dependents IS NULL THEN 1 ELSE 0 END) AS dependents_Null_Count,
    SUM(CASE WHEN Tenure IS NULL THEN 1 ELSE 0 END) AS Tenure_Null_Count,
    SUM(CASE WHEN PhoneService IS NULL THEN 1 ELSE 0 END) AS Phone_Service_Null_Count,
    SUM(CASE WHEN MultipleLines IS NULL THEN 1 ELSE 0 END) AS Multiple_Lines_Null_Count,
    SUM(CASE WHEN InternetService IS NULL THEN 1 ELSE 0 END) AS Internet_Service_Null_Count,
    SUM(CASE WHEN OnlineSecurity IS NULL THEN 1 ELSE 0 END) AS Online_Security_Null_Count,
    SUM(CASE WHEN OnlineBackup IS NULL THEN 1 ELSE 0 END) AS Online_Backup_Null_Count,
    SUM(CASE WHEN DeviceProtection IS NULL THEN 1 ELSE 0 END) AS Device_Protection_Null_Count,
    SUM(CASE WHEN TechSupport IS NULL THEN 1 ELSE 0 END) AS techsupport_Null_Count,
    SUM(CASE WHEN StreamingTV IS NULL THEN 1 ELSE 0 END) AS StreamingTV_Null_Count,
    SUM(CASE WHEN StreamingMovies IS NULL THEN 1 ELSE 0 END) AS Streaming_Movies_Null_Count,
    SUM(CASE WHEN Contract IS NULL THEN 1 ELSE 0 END) AS Contract_Null_Count,
    SUM(CASE WHEN PaperlessBilling IS NULL THEN 1 ELSE 0 END) AS PaperlessBilling_Null_Count,
    SUM(CASE WHEN PaymentMethod IS NULL THEN 1 ELSE 0 END) AS Payment_Method_Null_Count,
    SUM(CASE WHEN MonthlyCharges IS NULL THEN 1 ELSE 0 END) AS MonthlyCharge_Null_Count,
    SUM(CASE WHEN TotalCharges IS NULL THEN 1 ELSE 0 END) AS TotalCharges_Null_Count,
    SUM(CASE WHEN Churn IS NULL THEN 1 ELSE 0 END) AS Churn_Null_Count
FROM CustomerChurn;
 
 -- update
 update CustomerChurn
 set TotalCharges=(select avg(TotalCharges)from CustomerChurn)
 where TotalCharges is null;


-- view after update 
select * from CustomerChurn;

--null
SELECT 
    SUM(CASE WHEN CustomerID IS NULL THEN 1 ELSE 0 END) AS Customer_ID_Null_Count,
    SUM(CASE WHEN Gender IS NULL THEN 1 ELSE 0 END) AS Gender_Null_Count,
    SUM(CASE WHEN Partner IS NULL THEN 1 ELSE 0 END) AS partner_Null_Count,
    SUM(CASE WHEN SeniorCitizen IS NULL THEN 1 ELSE 0 END) AS seniorcitizen_Null_Count,
    SUM(CASE WHEN Dependents IS NULL THEN 1 ELSE 0 END) AS dependents_Null_Count,
    SUM(CASE WHEN Tenure IS NULL THEN 1 ELSE 0 END) AS Tenure_Null_Count,
    SUM(CASE WHEN PhoneService IS NULL THEN 1 ELSE 0 END) AS Phone_Service_Null_Count,
    SUM(CASE WHEN MultipleLines IS NULL THEN 1 ELSE 0 END) AS Multiple_Lines_Null_Count,
    SUM(CASE WHEN InternetService IS NULL THEN 1 ELSE 0 END) AS Internet_Service_Null_Count,
    SUM(CASE WHEN OnlineSecurity IS NULL THEN 1 ELSE 0 END) AS Online_Security_Null_Count,
    SUM(CASE WHEN OnlineBackup IS NULL THEN 1 ELSE 0 END) AS Online_Backup_Null_Count,
    SUM(CASE WHEN DeviceProtection IS NULL THEN 1 ELSE 0 END) AS Device_Protection_Null_Count,
    SUM(CASE WHEN TechSupport IS NULL THEN 1 ELSE 0 END) AS techsupport_Null_Count,
    SUM(CASE WHEN StreamingTV IS NULL THEN 1 ELSE 0 END) AS StreamingTV_Null_Count,
    SUM(CASE WHEN StreamingMovies IS NULL THEN 1 ELSE 0 END) AS Streaming_Movies_Null_Count,
    SUM(CASE WHEN Contract IS NULL THEN 1 ELSE 0 END) AS Contract_Null_Count,
    SUM(CASE WHEN PaperlessBilling IS NULL THEN 1 ELSE 0 END) AS PaperlessBilling_Null_Count,
    SUM(CASE WHEN PaymentMethod IS NULL THEN 1 ELSE 0 END) AS Payment_Method_Null_Count,
    SUM(CASE WHEN MonthlyCharges IS NULL THEN 1 ELSE 0 END) AS MonthlyCharge_Null_Count,
    SUM(CASE WHEN TotalCharges IS NULL THEN 1 ELSE 0 END) AS TotalCharges_Null_Count,
    SUM(CASE WHEN Churn IS NULL THEN 1 ELSE 0 END) AS Churn_Null_Count
FROM CustomerChurn;


-- CHURN BY INTERNET SERVICE TYPE
SELECT InternetService, 
       COUNT(*) AS TotalCustomers,
       SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS Churned,
       ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS ChurnRate
FROM CustomerChurn
GROUP BY InternetService
ORDER BY ChurnRate DESC;


-- CHURN BY TECH SUPPORT AVAILABILITY
SELECT TechSupport, 
       COUNT(*) AS TotalCustomers,
       SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS Churned,
       ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS ChurnRate
FROM CustomerChurn
GROUP BY TechSupport
ORDER BY ChurnRate DESC;


-- CHURN BY PAYMENT METHOD
SELECT PaymentMethod, 
       COUNT(*) AS TotalCustomers,
       SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS Churned,
       ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS ChurnRate
FROM CustomerChurn
GROUP BY PaymentMethod
ORDER BY ChurnRate DESC;