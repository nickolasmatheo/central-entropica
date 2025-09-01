<?php
// Arquivo de Configuração do Banco de Dados

// Definições do servidor local (XAMPP)
define('DB_SERVER', 'localhost');
define('DB_USERNAME', 'root'); // Usuário padrão do XAMPP
define('DB_PASSWORD', '');     // Senha padrão do XAMPP é vazia
define('DB_NAME', 'sociedade_db');

// Tenta criar a conexão com o banco de dados
$link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);

// Verifica a conexão
if($link === false){
    die("ERRO: Não foi possível conectar ao banco de dados. " . mysqli_connect_error());
}
?>