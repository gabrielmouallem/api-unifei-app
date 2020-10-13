Your app should now be running on [localhost:8000](http://localhost:8000/).

# Criar Banco de Dados

    linux: sudo -u postgres psql
    windows: .\psql.exe -U postgres
    drop database unifeiapp;
    CREATE DATABASE unifeiapp;
    CREATE USER unifeiapp WITH PASSWORD 'unifeiapp123';
    ALTER ROLE unifeiapp SET client_encoding TO 'utf8';
    ALTER ROLE unifeiapp SET default_transaction_isolation TO 'read committed';
    ALTER ROLE unifeiapp SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE unifeiapp TO unifeiapp;
    ALTER USER unifeiapp CREATEDB;

    *Esses comandos podem ser feitos através do PgMyAdmin ao invés da linha de comando acima*
    


# Importar Banco de Dados
### Linux:
    pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -d unifei-app unifei-app.db

### Windows:
    "C:\Program Files\PostgreSQL\10\bin\pg_restore" --verbose --clean --no-acl --no-owner -h localhost -U postgres -d unifei-app prod_3.db

Obs: dump no Windows

    "C:\Program Files\PostgreSQL\10\bin\pg_dump" -Fc --no-acl --no-owner -h localhost -U postgres unifei-app > local.dump

Somente então migrar o banco

    python manage.py migrate
    
# Criar novo superusuário
    
    Cada membro da equipe deve criar um superusuário para ter acesso a tudo que o django oferece
    python manage.py createsuperuser
    
# Página de Administrador do Django

    http://localhost:8000/admin/
    Logar com o superusuário
    
# Comandos Importantes !!

    python manage.py runserver        # Rodar o banco localmente
    
    python manage.py makemigrations   # Rodar SEMPRE que um modelo django for modificado
                                      # Pois ele faz o modelo se transformar no novo modelo no postgres
    
    python manage.py migrate          # Finalmente migra as mudanças pro postgres, o makemigrations cria
                                      # o que precisa ser mudado, e este comando muda finalmente no postgres
    
    **IMPORTANTE**: SEMPRE QUE FOR REALIZADA A MAKEMIGRATIONS COMMITAR AS MUDANÇAS PRO GIT
    
# Exemplos de Models
    
    class Profile(models.Model):
        '''
        Essa classe é um Perfil de usuário, relacionada a um User do sistema.
        Ela apresenta dados de contato, endereço, etc.
        '''
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        email = models.EmailField(unique=True)
        name = models.CharField(max_length=50, blank=True, null=True)
        birth = models.DateField(blank=True, null=True)
        #
        country = models.CharField(max_length=100, default='', blank=True, null=True)
        state = models.CharField(max_length=100, default='', blank=True, null=True)
        city = models.CharField(max_length=100, default='', blank=True, null=True)
        district = models.CharField(max_length=100, default='', blank=True, null=True)
        address_1 = models.TextField(blank=True, null=True)
        address_2 = models.TextField(blank=True, null=True)
        number = models.CharField(max_length=10, default='', blank=True, null=True)
        postal_code = models.CharField(max_length=8, validators=[RegexValidator(r'^\d{1,10}$')], default='',
                                       null=True, blank=True)
        #
        phone = models.CharField(max_length=20, blank=True, null=True)
        prefix_cell_phone = models.CharField(max_length=20, blank=True, null=True)
        cell_phone = models.CharField(max_length=20, blank=True, null=True)
        cpf = models.CharField(max_length=11, blank=True, null=True)
        created = models.DateTimeField(auto_now_add=True, editable=False, blank=True)
        sms_notification = models.BooleanField(default=True, )
        #success_msg = models.BooleanField(default=True, )
        #warning_msg = models.BooleanField(default=True, )
    
        client = models.IntegerField(default=0, choices=[(0, 'Irricontrol'), (1, 'Bauer')])
    
        class Meta:
            ordering = ('name',)

# Exemplos de serializers
    
    Genérico: o usuário envia todos os campos que possuem atributo obrigatório no modelo
    
    class ExemploSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exemplo
        fields = ['__all__']
        
    ____________________________________________________________________________
        
    Específico: o usuário quer editar apenas algum atributo específico da tabela
    
    class ExeemploSerializer(serializers.ModelSerializer):
    pivot = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Exemplo
        fields = ['descrição', 'tipo']

# Exemplos de Views

    SEM O REST FRAMEWORK: Feita sem ajuda do REST Framework para obter resultados especificos no qual
    podemos filtrar algum atributo que não queremos mostrar para o usuário ou algo
    nesse sentido.
    
    Um caso em que ele usa APIView na qual não faz parte das classes que possui tudo
    pronto do REST Framework, tendo que definir o método HTTP no qual essa view irá
    aceitar e definir tudo que será realizado neste método, neste caso o GET.

    class ExemploView(APIView):

    permission_classes = (IsAuthenticated,)  # Classes que verificam se o user está logado
    authentication_classes = (BearerToken,)  # Classes que verificam se o token de login ainda é valido

    def get(self, request):
        body = json.loads(request.body)                  # Pega os dados recebidos no corpo da requisição
        exemplo = Exemplo.objects.get(id=body['id'])     # Busca o objeto no banco que tem esse ID
        return Response(exemplo.descrição)               # Finalmente pega a descrição do obbjeto e retorna como resposta
        
    _____________________________________________________________________________________________________________________

     COM O REST FRAMEWORK: Feita com o REST Framework ele nos oferece classes que fazem todo o trabalho para a gente
    
    A CreateAPIView por exemplo seu próprio nome ja diz, para criar um novo objeto no banco
    
    A ListAPIView para listar todos os objetos do banco
    ... e assim por diante (documentação Django Rest)
    
    class ExemplosAPIView(ListAPIView):
        permission_classes = (IsAuthenticated,)
        authentication_classes = (BearerToken,)
    
        model = Exemplo
        serializer_class = ExemploSerializer # Usa o serializer pra transformar o objeto django em tabela do postgres
                                             # Com isso automaticamente ja temos tudo pronto e a lista foi retornada
    
    class ProfileCreateAPIView(CreateAPIView):       
        permission_classes = (IsAuthenticated,)
        authentication_classes = (BearerToken,)
    
        model = Exemplo
        serializer_class = ExemploSerializer # Usa o serializer pra transformar o resultado do postgres em algo que o django reconheça
                                             # Com isso automaticamente ja temos tudo pronto e a lista foi retornada
    