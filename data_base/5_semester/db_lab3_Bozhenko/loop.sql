-- select * from author;

DO $$
 DECLARE
     author_id   author.author_id%TYPE;
	 origin author.author_geo_origin%TYPE;
 BEGIN
     author_id := 100000000;
     origin := 'NY';
     FOR counter IN 1..10
         LOOP
		 	if counter > 5 then
				origin := 'MG';
			end if;
			
            INSERT INTO author (author_id, author_geo_origin)
            VALUES (counter + author_id, origin);
         END LOOP;
 END;
 $$
