<?php
// Inicializa a sessão
session_start();
 
// Verifica se o usuário está logado, se não, redireciona para a página de login
if(!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== true){
    header("location: index.php");
    exit;
}
?>
 
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Bem-vindo</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="home-content">
            <h1>Olá, <b><?php echo htmlspecialchars($_SESSION["username"]); ?></b>!</h1>
            <p>Bem-vindo à sua central de projetos, fóruns e arquivos. Aqui começa a sua área restrita!</p>
            <p>
                <a href="logout.php" class="btn">Sair da Conta</a>
            </p>
        </div>
    </div>
</body>
</html>