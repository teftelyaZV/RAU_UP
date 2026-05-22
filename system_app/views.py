from django.shortcuts import render, redirect
from .models import Tickets, Users, Administrators, TechSpecialists, Equipments, EquipmentStatus, TicketEquipment
from datetime import datetime


def login_page(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')

        try:
            admin = Administrators.objects.get(login=login, password=password)
            request.session['user_id'] = admin.id
            request.session['role'] = 'admin'
            return redirect('admin_dashboard')
        except Administrators.DoesNotExist:
            pass

        try:
            tech = TechSpecialists.objects.get(login=login, password=password)
            request.session['user_id'] = tech.id
            request.session['role'] = 'tech'
            return redirect('tech_dashboard')
        except TechSpecialists.DoesNotExist:
            pass

        try:
            user = Users.objects.get(login=login, password=password)
            request.session['user_id'] = user.id
            request.session['role'] = 'user'
            return redirect('user_dashboard')
        except Users.DoesNotExist:
            pass

        return render(request, 'login.html', {'error': 'Неверный login или пароль'})

    return render(request, 'login.html')


def user_dashboard(request):
    if request.session.get('role') != 'user':
        return redirect('login_page')

    if request.method == 'POST':
        equipment_ids = request.POST.getlist('equipment_ids')
        description = request.POST.get('description')
        audience = request.POST.get('audience')

        if equipment_ids and equipment_ids[0]:
            ticket = Tickets()
            ticket.Users_id_id = request.session['user_id']
            ticket.TechSpecialists_id = None

            try:
                admin = Administrators.objects.get(id=1)
                ticket.Administrators_id_id = admin.id
            except Administrators.DoesNotExist:
                first_admin = Administrators.objects.first()
                if first_admin:
                    ticket.Administrators_id_id = first_admin.id
                else:
                    admin = Administrators.objects.create(
                        login='temp_admin',
                        password='temp_pass'
                    )
                    ticket.Administrators_id_id = admin.id

            ticket.description = description
            ticket.audience = audience
            ticket.status = 'Новая'
            ticket.date_added = datetime.now()
            ticket.save()

            for equipment_id in equipment_ids:
                if equipment_id:
                    try:
                        equipment = Equipments.objects.get(id=equipment_id)
                        # Статус "Не исправно" (ID=3)
                        try:
                            broken_status = EquipmentStatus.objects.get(id=3)
                            equipment.status = broken_status
                            equipment.save()
                        except:
                            pass

                        TicketEquipment.objects.create(
                            ticket=ticket,
                            equipment=equipment
                        )
                    except:
                        pass

    my_tickets = Tickets.objects.filter(Users_id_id=request.session['user_id']).order_by('-date_added')

    for ticket in my_tickets:
        ticket.equipment_list = ticket.equipment_items.all()

    all_equipment = Equipments.objects.all()

    context = {
        'tickets': my_tickets,
        'equipment_list': all_equipment
    }
    return render(request, 'user_dashboard.html', context)


def admin_dashboard(request):
    if request.session.get('role') != 'admin':
        return redirect('login_page')

    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        tech_id = request.POST.get('tech_id')

        ticket = Tickets.objects.get(id=ticket_id)
        ticket.TechSpecialists_id_id = tech_id
        ticket.status = 'В процессе'
        ticket.save()

    all_tickets = Tickets.objects.all().order_by('-date_added')

    for ticket in all_tickets:
        ticket.equipment_list = ticket.equipment_items.all()

    all_techs = TechSpecialists.objects.all()
    all_equipment = Equipments.objects.all()

    context = {
        'tickets': all_tickets,
        'techs': all_techs,
        'equipment_list': all_equipment
    }
    return render(request, 'admin_dashboard.html', context)


def tech_dashboard(request):
    if request.session.get('role') != 'tech':
        return redirect('login_page')

    if request.method == 'POST':
        if 'ticket_id' in request.POST and 'action' in request.POST:
            ticket_id = request.POST.get('ticket_id')
            action = request.POST.get('action')
            ticket = Tickets.objects.get(id=ticket_id)

            if action == 'start_repair':
                ticket.status = 'На ремонте'
                ticket.save()

                # Меняем статус оборудования на "На ремонте" (ID=2)
                for ticket_equipment in ticket.equipment_items.all():
                    equipment = ticket_equipment.equipment
                    try:
                        repair_status = EquipmentStatus.objects.get(id=2)
                        equipment.status = repair_status
                        equipment.save()
                    except:
                        pass

            elif action == 'repaired':
                ticket.status = 'Отремонтирован'
                ticket.date_closed = datetime.now()
                ticket.save()

                # Меняем статус оборудования на "Исправно" (ID=1)
                for ticket_equipment in ticket.equipment_items.all():
                    equipment = ticket_equipment.equipment
                    try:
                        working_status = EquipmentStatus.objects.get(id=1)
                        equipment.status = working_status
                        equipment.save()
                    except:
                        pass

            elif action == 'unrepairable':
                ticket.status = 'Невозможно отремонтировать'
                ticket.date_closed = datetime.now()
                ticket.save()

                # Меняем статус оборудования на "Не исправно" (ID=3)
                for ticket_equipment in ticket.equipment_items.all():
                    equipment = ticket_equipment.equipment
                    try:
                        broken_status = EquipmentStatus.objects.get(id=3)
                        equipment.status = broken_status
                        equipment.save()
                    except:
                        pass

    my_tickets = Tickets.objects.filter(
        TechSpecialists_id=request.session['user_id']
    ).exclude(status__in=['Отремонтирован', 'Невозможно отремонтировать']).order_by('-date_added')

    for ticket in my_tickets:
        ticket.equipment_list = ticket.equipment_items.all()

    context = {
        'tickets': my_tickets
    }
    return render(request, 'tech_dashboard.html', context)


def logout(request):
    request.session.flush()
    return redirect('login_page')