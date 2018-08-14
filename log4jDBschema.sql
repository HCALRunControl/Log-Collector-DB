-- This SQL script creates the required tables by org.apache.log4j.db.DBAppender and
      -- org.apache.log4j.db.DBReceiver.
      --
      -- It is intended for Oracle databases.
      
      -- Tested successfully on Oracle9i Release 9.2.0.3.0 by James Stauffer
      
      -- The following lines are useful in cleaning any previous tables
      
	drop TRIGGER log_event_id_seq_trig;
	drop SEQUENCE log_event_id_seq;
	drop table log_event_property;
	drop table log_event_exception;
	drop table log_event;
	
	
	CREATE SEQUENCE log_event_id_seq MINVALUE 1 START WITH 1;
	
	CREATE TABLE log_event
	  (
	    session_id        NUMBER(20) NOT NULL,
	    timestamp         TIMESTAMP NOT NULL,
	    message           VARCHAR2(4000) NOT NULL,
	    logger_name       VARCHAR2(254) NOT NULL,
	    level_string      VARCHAR2(254) NOT NULL,
	    ndc               VARCHAR2(4000),
	    thread_name       VARCHAR2(254),
	    reference_flag    SMALLINT,
	    caller_filename   VARCHAR2(254) NOT NULL,
	    caller_class      VARCHAR2(254),
	    caller_method     VARCHAR2(254),
	    caller_line       CHAR(4) NOT NULL,
	    id                VARCHAR2(254) PRIMARY KEY
	  );
	
	
	CREATE TRIGGER log_event_id_seq_trig
	  BEFORE INSERT ON log_event
	  FOR EACH ROW 
	  BEGIN 
	    SELECT log_event_id_seq.NEXTVAL
	    INTO   :NEW.id
	    FROM   DUAL; 
	  END log_event_id_seq_trig;
	/
    
	CREATE TABLE log_event_property
	  (
	    event_id          VARCHAR2(254) NOT NULL,
	    mapped_key        VARCHAR2(254) NOT NULL,
	    mapped_value      VARCHAR2(1024),
	    PRIMARY KEY(event_id, mapped_key),
	    FOREIGN KEY (event_id) REFERENCES log_event(id)
	  );
	 
	CREATE TABLE log_event_exception
	  (
	    event_id         VARCHAR2(254) NOT NULL,
	    i                SMALLINT NOT NULL,
	    trace_line       VARCHAR2(254) NOT NULL,
	    PRIMARY KEY(event_id, i),
	    FOREIGN KEY (event_id) REFERENCES log_event(id)
	  );
