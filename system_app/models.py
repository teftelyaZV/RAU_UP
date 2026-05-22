from django.db import models


class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100)

#ZV
class Users(models.Model):
    id = models.AutoField(primary_key=True)
    FullName = models.CharField(max_length=100)
    Roles_id = models.ForeignKey(Roles, on_delete=models.CASCADE)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class EquipmentStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=50)


class Equipments(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.ForeignKey(EquipmentStatus, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField()


class Administrators(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class TechSpecialists(models.Model):
    id = models.AutoField(primary_key=True)
    FullName = models.CharField(max_length=100)
    competition = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class Tickets(models.Model):
    id = models.AutoField(primary_key=True)
    Users_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    TechSpecialists_id = models.ForeignKey(TechSpecialists, on_delete=models.SET_NULL, null=True, blank=True)
    Administrators_id = models.ForeignKey(Administrators, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=100)
    date_added = models.DateTimeField()
    date_closed = models.DateTimeField(null=True, blank=True)
    audience = models.CharField(max_length=100, blank=True, null=True)


class TicketEquipment(models.Model):
    id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE, related_name='equipment_items')
    equipment = models.ForeignKey(Equipments, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('ticket', 'equipment')