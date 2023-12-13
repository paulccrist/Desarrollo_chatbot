CREATE DATABASE IF NOT EXISTS app_ia;
USE app_ia;

CREATE TABLE usuarios (
    idusuarios INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(50) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    contraseña VARCHAR(255) NOT null);   
   
create table conversacion(
    id_conversacion INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL,
    respuestas TEXT,
    palabras_clave VARCHAR(50) NOT NULL
);
CREATE TABLE historial (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mensaje_usuario VARCHAR(500) NOT NULL,
    mensaje_bot VARCHAR(500) NOT NULL,
    fecha DATETIME NOT NULL
);
 
select * from usuarios;

show tables;