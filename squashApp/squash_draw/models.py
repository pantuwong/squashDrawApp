from django.db import models
import datetime

# Create your models here.

# model for player table
class Player( models.Model ):

    STATUS_CHOICES = [
        ( 'Active', 'Active' ),
        ( 'Inactive', 'Inactive' ),
        ( 'Away', 'Away')
    ]

    CLASS_CHOICES = [
        ( 'Juniors', 'Juniors' ),
        ( 'Seniors', 'Seniors' )
    ]

    # list of all attributes in the player table
    pySquashCode = models.CharField( max_length=10, blank=True, null=True )
    pyName = models.CharField( max_length=100 )
    pyRank = models.IntegerField( )
    pyGradedFlag = models.NullBooleanField()
    pyGrade = models.CharField( max_length=10, blank=True, null=True )
    pyPoint = models.IntegerField( blank=True, null=True )
    pyNote = models.CharField( max_length=10000, blank=True, null=True )
    pyTimeMustGreater = models.TimeField( blank=True, null=True )
    pyTimeMustLower = models.TimeField( blank=True, null=True )
    pyPlayTwiceFlag = models.NullBooleanField()
    pyMemberFlag = models.NullBooleanField()
    pyStatus = models.CharField( max_length=10, choices=STATUS_CHOICES, default='Active' )
    pyClass = models.CharField( max_length=10, choices=CLASS_CHOICES, default='Juniors' )

    # difine string representation for this model class, 
    # will be used when display model class data in dajango admin web site. 
    def __str__( self ):

        # would like display name on the admin site
        ret = self.pyName
        return ret

    def save(self, *args, **kwargs):
        super(Player, self).save(*args, **kwargs)
        rh = RankHistory(rhPlayer=self, rhDate=datetime.date.today(), rhRank=self.pyRank)
        rh.save()
        
# model for schedule
class Schedule( models.Model ):

    # list of all attributes in the schedule table
    scClass = models.CharField( max_length=20 )
    scDate = models.DateField()
    scTime = models.TimeField()
    scTimeBreak = models.BooleanField( default=True )
    scPlayer1Score = models.IntegerField( default = 0 )
    scPlayer2Score = models.IntegerField( default = 0 )
    scPlayer1Name = models.CharField( max_length=100,null=True, blank=True )
    scPlayer1Rank = models.IntegerField(null=True, blank=True)
    scPlayer2Name = models.CharField( max_length=100, null=True, blank=True)
    scPlayer2Rank = models.IntegerField(null=True, blank=True )
    scPlayer1 = models.ForeignKey( 'Player', related_name='player1_info', on_delete=models.SET_NULL, null=True, blank=True )
    scPlayer2 = models.ForeignKey( 'Player', related_name='player2_info', on_delete=models.SET_NULL, null=True, blank=True )
    scDraft = models.BooleanField( default=True )


    def __str__( self ):

        # get player1 name
        player1Name =  self.scPlayer1.pyName if self.scPlayer1 else scPlayer1Name

        # get player2 name
        player2Name = self.scPlayer2.pyName if self.scPlayer2 else scPlayer2Name

        return '{} ({}) - VS - ({}) {} ( on {} at {} )'.format( player1Name, self.scPlayer1Score, self.scPlayer2Score, player2Name, self.scDate, self.scTime )

# model for class rank history
class RankHistory( models.Model ):
    
    # list of field
    rhPlayer = models.ForeignKey( 'Player', related_name='player_info', on_delete=models.SET_NULL, null=True, blank=True )
    rhDate = models.DateField()
    rhRank = models.IntegerField()
    rhPlayerName= models.CharField( max_length=100, null=True, blank=True )

    def __str__( self ):
        # get player name
        playerName = self.rhPlayer.pyName if self.rhPlayer else self.rhPlayerName
        return '{} : {} ({})'.format(self.rhDate, playerName, self.rhRank)






















































