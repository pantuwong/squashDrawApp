from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('drawmatch', views.drawmatch, name='drawmatch'),
    path('drawmatch_backend', views.drawmatch_backend, name='drawmatch_backend'),
    path('generate_pdf', views.generate_pdf, name='generate_pdf'),
    path('genpdf_backend', views.genpdf_backend, name='genpdf_backend') ,
    path('record_score', views.record_score, name='record_score'),
    path('record_score_backend', views.record_score_backend, name='record_score_backend'),
    path('view_players', views.view_players, name='view_players'),
    path('add_player', views.add_player, name='add_player'),
    path('view_player', views.view_player, name='view_player'),
    path('edit_player', views.edit_player, name='edit_player'),
    path('edit_player_backend', views.edit_player_backend, name='edit_player_backend'),
    path('delete_player', views.delete_player, name='delete_player'),
    path('success', views.success, name='success'),
    path('fail', views.fail, name='fail'),
    path('match_history', views.match_history, name='match_history'),
    path('edit_schedule', views.edit_schedule, name='edit_schedule'),
    path('save_schedule', views.save_schedule, name='save_schedule'),
    path('view_schedule', views.view_schedule, name='view_schdeule'),
    path('delete_schedule', views.delete_schedule, name='delete_schedule'),
    path('delete_match', views.delete_match, name='delete_match'),
    path('delete_match_enter_score', views.delete_match_enter_score, name='delete_match_enter_score'),
    path('edit_match_enter_score', views.edit_match_enter_score, name='edit_match_enter_score'),
    path('edit_match_enter_score_backend', views.edit_match_enter_score_backend, name='edit_match_enter_score_backend'),
    path('list_draw', views.list_draw, name='list_draw')
]
