"""empty message

Revision ID: b41e68178be9
Revises: 
Create Date: 2021-08-24 12:19:23.653908

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.

from models import User, user

revision = 'b41e68178be9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Creating a table for all users.
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('user_role', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('username'),
                    sa.UniqueConstraint('email'),
                    )

    # Creating a table for all posts.
    op.create_table('post',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('created_date', sa.DateTime(), nullable=False),
                    sa.Column('edited_date', sa.DateTime(), nullable=False),
                    sa.Column('created_by', sa.Integer(), nullable=False),
                    sa.Column('edited_by', sa.Integer(), nullable=True),
                    sa.Column('short_content', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
                    sa.ForeignKeyConstraint(['edited_by'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('title')
                    )

    # Creating a table for all comments.
    op.create_table('comment',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.Column('parent', sa.Integer(), nullable=True),
                    sa.Column('created_date', sa.DateTime(), nullable=False),
                    sa.Column('author_id', sa.Integer(), nullable=True),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
                    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    )

    # Populate the table with some initial data.
    _user = sa.table('user',
                     sa.column('id', sa.Integer),
                     sa.column('username', sa.String),
                     sa.column('email', sa.String),
                     sa.column('password', sa.Date),
                     sa.column('user_role', sa.Integer),
                     )

    _post = sa.table('post',
                     sa.column('id', sa.Integer),
                     sa.column('title', sa.String),
                     sa.column('content', sa.String),
                     sa.column('created_date', sa.DateTime),
                     sa.column('edited_date', sa.DateTime),
                     sa.column('created_by', sa.Integer),
                     sa.column('short_content', sa.String),
                     )

    _comment = sa.table('comment',
                        sa.column('id', sa.Integer),
                        sa.column('post_id', sa.Integer),
                        sa.column('author_id', sa.Integer),
                        sa.column('parent', sa.Integer),
                        sa.column('content', sa.String),
                        sa.column('created_date', sa.DateTime)
                        )

    op.bulk_insert(_user,
                   [
                       {'id': 1,
                        'username': 'admin',
                        'email': 'admin@admin.com',
                        'password': '17824887c2eb6901a003d27c52c824114ae4804f7b56ca4894719c46',
                        'user_role': 3},
                       {'id': 2,
                        'username': 'author',
                        'email': 'author@author.com',
                        'password': '4f555b1bb8bc729a665b8892df73119e2ef2eb50dffaf0d5c546cf23',
                        'user_role': 2}
                   ]
                   )

    # I'm defining a current time variable because otherwise using `datetime.now()` twice would result in two different times.
    cur_time = datetime.now()
    op.bulk_insert(_post,
                   [
                       {'id': 1, 'title': 'SpareRibs volgens de 3-2-1 Methode',
                        'short_content': 'Leer in een handomdraai de beste spare-ribs te maken die je ooit hebt gegeten. Ik durf te wedden dat je na het proberen van deze snack verpest bent en nergens meer zulke lekkere spareribs kan eten.',
                        'content': "<p> De 3-2-1 Methode bij het garen van spareribs staat voor de tijdsblokken van de 3 verschillende processen. Bij de spareribs zoals wij ze in Nederland kennen kunnen we uitgaan dat 1 eenheid circa 45 minuten is. De eerste stap duurt dus 2 uur en 3 kwartier, waar de 2e stap 1,5 uur duurt, en de laatste stap (op papier) 45 minuten. </p><span> <h3>De rub</h3> <p> We beginnen met een lekkere rub. Deze rub maken we met de volgende ingrediënten: </p><ul> <li>1 eetlepel zout</li><li>1 eetlepel zwarte peper</li><li>1 eetlepel knoflookpoeder</li><li>1 eetlepel paprikapoeder</li><li>1 eetlepel chillipoeder</li></ul> <p> Nu de we de rub hebben beginnen we met de voorbereiding van de spareribs. We beginnen door het vlies van de onderzijde te verwijderen. Ik vind dit altijd het makkelijkste gaan met een stukje keukenpapier. Zodra we dit hebben gedaan brengen we een laagje zonnebloemolie aan op de spareribs waarna we deze bestrooien met onze dry rub. </p><p> Het is nu zaak om de BBQ, Smoker of kamado op te stoken. De ribs gaan we klaarmaken via indirecte methode. Ik ga er bij deze vanuit dat jullie weten hoe dit werkt, en anders maak ik hier later nog wel een post over ;). Zodra de ketel aan het opwarmen is heb je tijdens het wachten een mooi excuus om een biertje open te trekken. Bij lekker weer zou ik een lekkere Desparados suggereren! </p><p>Zodra de BBQ rond de 120 graden zit en stabiel blijft mogen de ribjes erop en beginnen we met de rookfase. Deze laten wij voor circa 2 uur en 3 kwartier liggen.</p><p> Na deze periode mogen de ribjes eraf. We gaan ze nu inpakken in alumininium folie. Voor een extra lekkere smaak raad ik aan om een scheutje appelsap of dubbelfris bij de sparerib te doen. Zorg er voor dat de folie zo STRAK mogelijk om de rib heen zit. Als je dit gedaan hebt mogen de ribjes terug voor circa 1.5 uur. </p><p> Haal de ribjes er weer af, en haal ze voorzichtig uit de folie. Maar pas op! De ribs zijn nu zacht en snotgaar. Het zou zonde zijn als ze nu uit elkaar vallen. Zodra je ze uit de folie hebt leggen we ze weer terug op de BBQ en lakken we ze af in de saus. Ik vind hierbij zwarte pepersaus meestal het lekkerste. We gaan hier wel een beetje smokkelen, officieel zou het laatste blok voor 45 minuten staan. Maar na die 45 minuten is de saus verbrand. In principe zou een minuutje of 10 meer dan voldoende moeten zijn om een lekkere krokante bark te kunnen creeëren. </p><p>Als deze 10 minuutjes voorbij zijn halen we de ribs er weer af en laten we deze voor circa 20 minuten rusten. Hierna zijn ze klaar om op te eten. Enjoy!</p></span>",
                        'created_date': cur_time, 'edited_date': cur_time, 'created_by': 1}
                   ])

    op.bulk_insert(_comment,
                   [
                       {
                           'id': 1,
                           'post_id': 1,
                           'created_date': datetime.now(),
                           'author_id': 2,
                           'parent': None,
                           'content':
                               'Woah Mickael, Dit zijn de beste spareribs ooit. Ze doen me wel een beetje aan het recept van Noskos denken. Je zou zijn MOINK balls eens moeten proberen!'
                       },
                       {
                           'id': 2,
                           'post_id': 1,
                           'created_date': datetime.now(),
                           'author_id': 1,
                           'parent': 1,
                           'content': 'Sshh, niet doorvertellen!! Ja MOINK Balls zijn ook super!'}
                   ])


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    op.drop_table('user')
    op.drop_table('comment')
    # ### end Alembic commands ###
