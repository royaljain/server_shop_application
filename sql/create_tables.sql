CREATE TABLE company_attributes ( CompanyId text PRIMARY KEY NOT NULL, NumberOfEmployees int);
CREATE TABLE consumer_attributes ( ConsumerId text PRIMARY KEY NOT NULL, LastVisit date, NumberOfVisits INT, MoneySpent real, DiscountSaved real, CompanyId text REFERENCES company_attributes(CompanyID));
CREATE TABLE consumer_faces ( ConsumerId text PRIMARY KEY REFERENCES consumer_attributes(ConsumerId) NOT NULL, encodings real[]);

CREATE OR REPLACE FUNCTION distance(l real[], r real[]) RETURNS real AS $$
DECLARE
  s real;
BEGIN
  s := 0;
  FOR i IN 1..128 LOOP
    s := s + ((l[i] - r[i]) * (l[i] - r[i]));
  END LOOP;
  RETURN |/ s;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE dish_attributes (DishId text PRIMARY KEY NOT NULL);
CREATE TABLE store_attributes (StoreId text PRIMARY KEY NOT NULL, NumberOfEmployees INT, city text);
CREATE TABLE store_menu(StoreId text REFERENCES store_attributes(StoreId), DishId text REFERENCES dish_attributes(DishId), DishName text NOT NULL, DishDescription text NOT NULL, DishImage text NOT NULL, DishCategory text NOT NULL, SellingPrice float NOT NULL, Tag text, Rating float NOT NULL, Position INT NOT NULL);



CREATE TABLE employee_attributes (EmployeeId text PRIMARY KEY NOT NULL, Name text, Manager text, StoreId text REFERENCES store_attributes(StoreId), ScheduledTimeIn time, ScheduledTimeOut time, NumberOfDaysWorking int, AverageWorkingHour real);
CREATE TABLE employee_faces (EmployeeId text REFERENCES employee_attributes(EmployeeId), encodings real[]);
CREATE TABLE employee_register (EmployeeId text REFERENCES EmployeeAttributes(EmployeeId), EntryDate date, InTime time, OutTime time, IsLate int, IsOvertime int, HoursWorked interval); 


CREATE TABLE leave_list (date_of_leave date, reason text); 
