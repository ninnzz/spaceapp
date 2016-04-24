# MySQL Config
# For multiple mysql connections, use object for each config,
# the db driver will read and parse it as needed

MYSQL_EARNINGS = {
    'host': 'earnings-database.csbg4ppommmg.us-east-1.rds.amazonaws.com',
    'user': 'freedom',
    'password': '7eight910',
    'db': 'earnings',
    'port': 3306
}


MYSQL_MASTER = {
    'host': 'master-db.csbg4ppommmg.us-east-1.rds.amazonaws.com',
    'db': 'master',
    'user': 'freedom',
    'password': '7eight910focusonrevenue',
    'port': 3306
}


MYSQL_MUSIC = {
    'host': 'master-db.csbg4ppommmg.us-east-1.rds.amazonaws.com',
    'db': 'music_dashboard',
    'user': 'freedom',
    'password': '7eight910focusonrevenue',
    'port': 3306
}


ELASTIC_SEARCH = {
    'host': 'localhost',
    'port': 9200
}


# Freedom Accounts Config
FACCOUNTS_PARAMS = {
    'client_id': '47b67722-ce17-4706-99d3-60579d04ddea',
    'redirect_uri': 'http://api.tunes.tm/auth/callback',
    'response_type': 'code',
    'roles': 'profile,email,partner',
    'force_auth': 'true',
    'state': 'tunes'
}


# Email invite
EMAIL = {
    'subject': 'Invitation from Tunes.tm',
    'text': 'Log in to Tunes.tm',
    'html': {
        'admin': '''
                    Hi,
                    <br/><br/>
                    We are inviting you to join Tunes.tm and be the owner of the record label,
                    <a href="{mp_url}">{mp}</a>.
                ''',
        'music_provider': '''
                            Hi,
                            <br/><br/>
                            You are invited by the record label,
                            <a href="{mp_url}">{mp}</a> to join Tunes.tm and be one of their {role}s.
                        '''
    },
    'footer': '''
                <br/><br/>
                You may now log in to <a href="http://tunes.tm">Tunes.tm</a>
                by clicking on the link below or copying and pasting it in your browser:
                <br/><br/>
                <a href="http://tunes.tm/#/login">http://tunes.tm/#/login</a>
                <br/><br/>
                <img src="http://tunes.tm/images/email-banner.png"/>
            '''
}

# Frontend URL
FRONTEND_URL = 'http://tunes.tm'

# Frontend Freedom Callback URL
FRONTEND_LOGIN_CALLBACK_URL = FRONTEND_URL + '/#/login/callback'

# Record Label URL
RECORD_LABEL_URL = FRONTEND_URL + '/#/record-label'

# Music Provider URL
MUSIC_PROVIDER_URL = 'tunes.tm'
