CREATE ROLE django;
ALTER ROLE django WITH login encrypted password 'jessie+|=1nkman';
ALTER ROLE django WITH CREATEDB;

CREATE DATABASE django WITH OWNER django;
