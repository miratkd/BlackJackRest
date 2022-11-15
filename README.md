# BlackJackRest
BlackJaskRest é um back-end rest Python desenvolvido do zero utilizando o frameword Django-Rest. Todos os end-points são autorizados e autenticados com a ajuda
da biblioteca Django-OAuth-Toolkit, a biblioteca de implementação do padrão OAuth2 recomendada pela própria  documentação do framework Django. Todas as informações
das partidas, assim como o histórico delas e registros dos usuários são persistidos em um banco PostGresSQL hospedado com o site na plataforma Heroku, e pode ser
facilmente acessado através do admin próprio do framework Django. A API oferece todos os end-points para a criação de um jogo de black-jack (também conhecido no Brasil
como "21"), dês da criação dos usuários que serão usados no sistema, até o end-points para criar partida, sacar as carta, finalizar o round, etc.
 
 Para ver uma implementação completa desse Back-End, por favor de uma olhada também no projeto BlackJackRestFrontEnd, um
 site Single-Page-Aplication desenvolvido usando o framework VueJs que consome todos os end-points desse projeto.
 
 Abaixo segue a documentação da API.
 
 ----
 
 ## Criar usuário
 
 Um end-point público para criar os usuários do sistema.
 
 **POST**:  https://black-jack-rest.herokuapp.com/account/ 
 
 **BODY**:
 {
 
    "user": {
        "username": O nome de usuário da conta, esse valor será usado como chave primário, por isso, caso um username já utilizado for passado, o end-poit retornara um erro informando que o username já foi utilizado. 
        "email": E-mail associado a aquela conta.
        "password": Senha de acesso para a conta que vai ser criada, graças a framework Django, o que será salvo é uma versão encriptografada desse valor, tirando a necessidade do banco de dados salva a senha dos usuarios. 
    }
    
 }
 
 **Exemplos 1**:
 {
 
    "user": { 
        "username": "lucas123", 
        "email": "lucas123@gmail.com", 
        "password": "13972684" 
    } 
 
 }
 
  **Exemplos 2**:
  {
  
      "user": { 
        "username": "joaoGamer", 
        "email": "joaogamer@gmail.com", 
        "password": "hightcode" 
      } 
  
  }
  
  ## Login
  
  End-point para receber um access token de uma certa conta.
  
  **POST:** https://black-jack-rest.herokuapp.com/o/token/
  
  **HEADER:** {
  
      "Content-Type": application/x-www-form-urlencoded
      
  }
  
  **BODY:**{
  
      "grant_type": " password " 
      "Username": Mesmo username passado na hora de criar a conta. 
      "Password": Mesmo password passado na hora de criar a conta. 
      "client_id": Chave de acesso do cliente. 
      "client_secret": senha de acesso do cliente. 
  
  }
  
  **Exemplos 1**:
 {
 
    "grant_type": " password " 
    "Username": "lucas123" 
    "Password": "13972684" 
    "client_id": "vErNybWh2TVRitDgec4jnx1ZdkkdHETvMHFK7xm” 
    "client_secret":"CFJ3Ovq0rqOMLWUWajwKtRdnlxF3LIFvSzlQJ5VsIBYILXDnnmA8kmoPRfGmInbp2Y6hvXITG8LaPrFPh9QqkHvgNF8I1sA2Q4X54ewqzyIM4uWSLpuxg3uHvNPsyned " 
 
 }
 
  **Exemplos 2**:
  {
  
      "grant_type": " password " 
      "Username": "joaoGamer" 
      "Password": "hightcode" 
      "client_id": "vErNybWh2TVRitDgec4jnx1ZdkkdHETvMHFK7xm” 
      "client_secret":"CFJ3Ovq0rqOMLWUWajwKtRdnlxF3LIFvSzlQJ5VsIBYILXDnnmA8kmoPRfGmInbp2Y6hvXITG8LaPrFPh9QqkHvgNF8I1sA2Q4X54ewqzyIM4uWSLpuxg3uHvNPsyned" 
  
  }
  
  **Resposta:** {
  
      "access_token": Token que deve ser passado nos endpoints autenticados. 
      "expires_in": duração do token em segundos. 
      "refresh_token": esse token pode ser usado para receber um novo access_token, uma vez que o primeiro já tenha expirado. 
      "scope": nível de permissão do access_token 
      "token_type": tipo do access_token 
  
  }
  
  **Exemplo de resposta:**{
  
      "access_token": "0DuJ7oPKhDRsoIbzpCeyY5dkXVKfkb" 
      "expires_in": 36000 (10 horas) 
      "refresh_token": "M2MmP3JuyYgWnqAqkshe3nM4rg3ANA" 
      "scope": "read write groups" 
      "token_type": "Bearer" 
  
  }
  
  ## Autenticação e autorização.
  
  Todos os end-points (com exceção do end-point de criar usuário e o de login) são privados, ou seja, é obrigatório passar um access_token para ter acesso aquele end-point. 

  O sistema de autorização e autenticação é uma implementação simples do protocolo OAuth2, feita através da biblioteca "Django OAuth Toolkit" 

  Para ser autenticado pelo servidor é preciso passar o seguinte parâmetro no header da request: 
  { 

    " Authorization ": tipo do token + access_token  

  } 

**Exemplo:**
{ 

    " Authorization ": "Bearer 0DuJ7oPKhDRsoIbzpCeyY5dkXVKfkb " 

}

## Informações da conta. 

Retorna informações da conta equivalente a aquele access_token. 

**GET**: https://black-jack-rest.herokuapp.com/account/me/ 

**HEADER**: 
{

    " Authorization ": tipo do token + access_token
    
}

**BODY**: {}

**RESPOSTA**:  
{

    "Id": o ID daquela conta. 
    "Tickets": quantidade de tickets daquela conta. 
    "User": { 
      "email": email cadastrado a aquela conta. 
      "first_name": primeiro nome do dono da conta. 
      "is_active": estado da conta.
      "last_name": último nome do dono da conta. 
      "username": nome de usuário associado a aquela conta. 
    }

}

**Exemplo de resposta**:
{

    "Id": 01 
    "Tickets": 500 
    "User": { 
        "email": "lucas123@gmail.com", 
        "first_name": "lucas", 
        "is_active": "true", 
        "last_name": "mira", 
        "username": "lucas123" 
    } 

}

## Atualizar conta.

End-point para atualizar as informações de uma conta. 

**PUT**: https://black-jack-rest.herokuapp.com/account/{ACCOUNT-ID}/ 

**HEADER**: 
{

    " Authorization ": tipo do token + access_token

} 

**BODY**:
{

    "user": { 
        "first_name": novo primeiro nome para a conta, 
        "last_name": novo ultimo nome para a conta, 
        "email": novo email para a conta 
    }

}

**Exemplo de BODY**:
{

    "user": { 
        "first_name": "lucas", 
        "last_name": "mira", 
        "email": "mira2022@hotmail.com" 
    } 

}

**RESPOSTA**: mesma conta, agora com as informações atualizadas.

## Deletar conta. 

End-point para deletar uma conta do sistema (Esse sistema não possui nenhum tipo de "Desativar a contar" ou "Deixar a conta inativa", o end-point de deletar usuário irá excluir o usuário do banco de dados, assim como qualquer informação atrelada a ele.) 

**DELETE**: https://black-jack-rest.herokuapp.com/account/{ACCOUNT-ID}/ 

**HEADER**: 
{

    " Authorization ": tipo do token + access_token
    
} 

**BODY**: {} 

**RESPOSTA**: STATUS 204 sem nenhuma informação no BODY da resposta.

## Resgatar Ticket diário. 

Uma vez por dia, uma conta pode resgatar uma quantidade gratuita de tickets. 

**PUT**: https://black-jack-rest.herokuapp.com/account/redeem_daily_tickets/ 

**HEADER**: {

    " Authorization ": tipo do token + access_token
    
} 

**BODY**: {} 

**RESPOSTA**: 
{ 

    "account": Objeto com as informações da conta. 
    "message": Mensagem confirmando que os tickets foram adicionados a 	conta. 
    
} 

**Exemplo de resposta**: { 

    "account": { 
        "id": 1,
        "ticket": 700,
        ...
    } 
    "message": "Daily free tickets redeem." 

} 

## Criar uma partida.

End-point para criar uma partida de black-jack. 

**POST**: https://black-jack-rest.herokuapp.com/math/ 

**HEADER**: 
{

    " Authorization ": tipo do token + access_token
    
} 

**BODY**: { 

    "account": O id da conta que está criando a partida. 
    "buy_in_value": Valor que o usuário está apostando. 

} 

**Exemplo de BODY**: { 

    "account": 1 
    "buy_in_value": 50 

} 

**RESPOSTA**: { 

    "account": id da conta a qual esta partida está associada. 
    "date": Data em que a partida foi criada. 
    "dealer_hand": Lista de carta do "dealer" [ 
        0: { 
            "img_url": Imagem da carta. (Antes do usuário dar o "hold", a  primeira carta do "dealer fica escondida") 
            "position": Posição da carta. 
            "value": Numero representando valor da carta. 
        } 
        1: { 
            "hand": Id da mão associada a aquela carta. 
            "id": Id da carta. 
            "img_url": Imagem da carta. 
            "position": Posição da carta. 
            "value": Numero representando valor da carta. 
        } 
    ] 
    "id": Id da partida 
    "is_over": Booleano indicando se a partida acabou ou não. 
    "is_win": Booleano indicando se a partida foi uma vitória para o usuário. 
    "math_active_round": Numero indicando o round atual da partida. 
    "player_hand": Objeto contendo todas as informações sobre a mão do usuario.	{ 
        "cards": Lista contendo todas as cartas do usuario. [ 
            0: { 
                "hand": Id da mão associada a aquela carta. 
                "id": Id da carta. 
                "img_url": Imagem da carta. 
                "position": Posição da carta. 
                "value": Numero representando valor da carta. 
            } 
            1: { 
                "hand": Id da mão associada a aquela carta. 
                "id": Id da carta. 
                "img_url": Imagem da carta. 
                "position": Posição da carta. 
                "value": Numero representando valor da carta. 
            } 
        ]
        "id": Id da mão. 
        "is_hold": Booleano indicando se o usuário decidiu ficar com a mão. 
        "is_out": Booleano indicando se o usuário bateu. (pontuação da mão foi maior que 21.) 
        "is_player_hand": Booleano indicando se esta é a mão do usuário. 
        "math": Id da partida associada a esta mão. 
        "round": número indicando de qual round é aquela mão. 
        "total_point": Numero indicando a quantidade de pontos que aquela mão tem. (soma da pontuação de todas as cartas) 
    }
    "prize": Numero representando a quantidade de tickets que vai ser a recompensa por ganhar aquela partida. (A recompensa padra é três vezes o valor apostado.) 
    "rounds_won": Numero representando a quantidade de rounds que o usuário ganhou. 

} 

**Exemplo de resposta**:
{ 

    "account": 1 
    "date": "2022-10-24T14:33:36.203909-03:00" 
    "dealer_hand": [ 
        0: { 
            "img_url": "?" 
            "position": 0 
            "value": "?" 
        } 
        1: { 
            "hand": 26 
            "id": 345 
            "img_url": "7_of_clubs.svg" 
            "position": 1 
            "value": 7 
        } 
    ] 
    "id": 36 
    "is_over": false 
    "is_win": false 
    "math_active_round": 1 
    "player_hand":{ 
        cards: [ 
            0: { 
                "hand": 27 
                "id": 346 
                "img_url": "king_of_clubs.svg" 
                "position": 0 
                "value": 10 
            } 
            1: { 
                "hand": 27 
                "id": 347 
                "img_url": "king_of_spades.svg" 
                "position": 1 
                "value": 10 
            } 
        ]
        "id": 27 
        "is_hold": false 
        "is_out": false 
        "is_player_hand": true 
        "math": 36 
        "round": 1 
        "total_point": 20 
    } 
    "prize": 150 
    "rounds_won": 0 

} 

## Sacar uma carta. 

Uma nova carta vai ser adicionada a mão do jogador. 

**POST**: https://black-jack-rest.herokuapp.com/math/{MATH_ID}/draw_card/ 

**HEADER**: {

    " Authorization ": tipo do token + access_token
    
} 

**BODY**: { }

**RESPOSTA**: { Mesma resposta do end-point criar partida, agora com as informações 	atualizadas. }

## Manter a mão. 

End-point que permite ao jogador manter a mão atual e comparar com as cartas do dealer. ("HOLD") 

**POST**: https://black-jack-rest.herokuapp.com/math/{MATH_ID}/hold/ 

HEADER: {

    " Authorization ": tipo do token + access_token
    
} 

**BODY**: {} 

RESPOSTA { Mesma resposta do end-point criar partida, porem agora as cartas do 	dealer estarão visíveis, assim como o resultado do round. } 

## Passar o round. 

Finaliza o round atual, e inicia o próximo. 

**POST**: https://black-jack-rest.herokuapp.com/math/{MATH_ID}/next_round/ 

**HEADER**: {

    " Authorization ": tipo do token + access_token

} 

BODY: {} 

RESPOSTA: { Mesma resposta do end-point criar partida, porem agora com as informações no novo round ou o resultado da partida caso os rounds já tenham acabado. }


