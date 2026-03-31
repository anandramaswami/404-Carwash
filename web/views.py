from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from customers.models import Customers
from services.models import Services
from parking.models import Parking_Slots
from bookings.models import Booking_History

def home(request):
    return render(request, 'home.html')

def about_us(request):
    return render(request, 'about.html')

def services(request):
    services_list = Services.objects.all()
    return render(request, 'services.html', {'services': services_list})

@login_required
def my_bookings(request):
    if request.user.is_customer:
        customer = Customers.objects.filter(user=request.user).first()
        bookings = Booking_History.objects.filter(customer=customer)
        return render(request, 'my_bookings.html', {'bookings': bookings})
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        u_input = request.POST.get('username').strip()
        p = request.POST.get('password')
        
        # Try raw first (for admins or anyone with exact case)
        user = authenticate(request, username=u_input, password=p)
        
        # If raw fails, try uppercase (for normalized customers)
        if user is None:
            user = authenticate(request, username=u_input.upper(), password=p)
            
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            if user.is_admin:
                return redirect('admin_dashboard')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        u = request.POST.get('username').strip().upper()  # Force uppercase
        e = request.POST.get('email')
        p = request.POST.get('password')
        c = request.POST.get('contact')
        a = request.POST.get('address')
        
        if CustomUser.objects.filter(username=u).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = CustomUser.objects.create_user(username=u, email=e, password=p)
            user.is_customer = True
            user.save()
            # Also create customer profile
            c_id = f"M-{Customers.objects.count() + 101}"  # Starting from 101 for better aesthetics
            import random
            pin_val = f"{random.randint(0, 9999):04d}"
            Customers.objects.create(user=user, customer_id=c_id, customer_name=u, email=e, contact=c, address=a, payment_pin=pin_val)
            
            messages.success(request, 'Registration successful. Please log in with your new credentials.')
            return redirect('login')
    return render(request, 'register.html')

@login_required
def book_service(request, service_id):
    if not request.user.is_customer:
        messages.error(request, 'Only customers can book services.')
        return redirect('home')
        
    service = get_object_or_404(Services, id=service_id)
    available_slots = Parking_Slots.objects.filter(is_available=True)
    
    if request.method == 'POST':
        c_brand = request.POST.get('car_brand')
        c_model = request.POST.get('car_model')
        c_color = request.POST.get('car_color')
        c_reg = request.POST.get('car_reg_num')
        s_date_str = request.POST.get('service_date')
        parking_slot_id = request.POST.get('parking_slot')
        
        s_date = parse_date(s_date_str)
        
        # Get customer profile
        customer = Customers.objects.filter(user=request.user).first()
        
        # Instead of creating DB record, store in session
        request.session['pending_booking_data'] = {
            'service_id': service.id,
            'parking_slot_id': parking_slot_id,
            'service_date': s_date_str,
            'car_brand': c_brand,
            'car_model': c_model,
            'car_color': c_color,
            'car_reg_num': c_reg,
        }
        
        return redirect('process_payment')

    return render(request, 'book_service.html', {'service': service, 'available_slots': available_slots})

@login_required
def process_payment(request):
    data = request.session.get('pending_booking_data')
    if not data:
        messages.error(request, 'No active booking session found.')
        return redirect('home')

    service = get_object_or_404(Services, id=data['service_id'])
    customer = Customers.objects.filter(user=request.user).first()
    
    # Render with dummy object for GET
    class DummyBooking:
        def __init__(self):
            self.id = Booking_History.objects.count() + 1
            self.service = service
            self.service_date = parse_date(data['service_date'])
            self.car_brand = data['car_brand']
            self.car_model = data['car_model']
            self.car_color = data['car_color']
            self.car_reg_num = data['car_reg_num']
            self.parking = None
            if data['parking_slot_id']:
                self.parking = Parking_Slots.objects.filter(id=data['parking_slot_id']).first()

    booking = DummyBooking()
    
    if request.method == 'POST':
        # Now we create the booking and reserve the slot
        parking_slot = None
        if data['parking_slot_id']:
            parking_slot = get_object_or_404(Parking_Slots, id=data['parking_slot_id'])
            if parking_slot.is_available:
                parking_slot.is_available = False
                parking_slot.save()
            else:
                messages.error(request, 'This parking slot was just booked by someone else. Please start again.')
                return redirect('book_service', service_id=service.id)
                
        import uuid
        actual_booking = Booking_History.objects.create(
            customer=customer,
            service=service,
            parking=parking_slot,
            service_date=booking.service_date,
            car_brand=booking.car_brand,
            car_model=booking.car_model,
            car_color=booking.car_color,
            car_reg_num=booking.car_reg_num,
            booking_status='Booked',
            payment_status='Paid',
            payment_id=str(uuid.uuid4())
        )
        
        if 'pending_booking_data' in request.session:
            del request.session['pending_booking_data']
            
        messages.success(request, f'Payment successful! Your booking is confirmed. Order ID: {actual_booking.payment_id}')
        return redirect('my_bookings')
        
    return render(request, 'payment.html', {'booking': booking})

# Admin Views
@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        return redirect('home')
    
    context = {
        'customers_count': Customers.objects.count(),
        'bookings_count': Booking_History.objects.count(),
        'services_count': Services.objects.count(),
        'parkings_count': Parking_Slots.objects.count(),
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
def dashboard_customers(request):
    if not request.user.is_admin: return redirect('home')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            customer_id = request.POST.get('customer_id')
            try:
                customer = Customers.objects.get(id=customer_id)
                # First delete the custom user if needed, or just the customer profile
                # Typically deleting the user is cleaner if it's a 1-to-1
                if customer.user:
                    customer.user.delete()
                else:
                    customer.delete()
                messages.success(request, 'Customer deleted successfully.')
            except Customers.DoesNotExist:
                messages.error(request, 'Customer not found.')
        return redirect('dashboard_customers')

    query = request.GET.get('q', '')
    if query:
        customers = Customers.objects.filter(customer_name__icontains=query).order_by('-created_at')
    else:
        customers = Customers.objects.all().order_by('-created_at')
        
    return render(request, 'admin/dashboard_customers.html', {'customers': customers, 'query': query})

@login_required
def dashboard_bookings(request):
    if not request.user.is_admin: return redirect('home')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_status':
            booking_id = request.POST.get('booking_id')
            new_status = request.POST.get('status')
            try:
                booking = Booking_History.objects.get(id=booking_id)
                # Check if it was already in a final state
                if booking.booking_status in ['Completed', 'Cancelled']:
                    messages.error(request, f'This booking is already {booking.booking_status} and cannot be modified.')
                else:
                    booking.booking_status = new_status
                    
                    # Dynamic Parking Slot Management - Release when Completed/Cancelled
                    if booking.parking:
                        parking = booking.parking
                        if new_status == 'Booked':
                            parking.is_available = False
                        elif new_status in ['Completed', 'Cancelled']:
                            parking.is_available = True
                        parking.save()
                    
                    booking.save()
                    messages.success(request, f'Booking status updated to {new_status}.')
            except Booking_History.DoesNotExist:
                messages.error(request, 'Booking not found.')
        return redirect('dashboard_bookings')
        
    bookings = Booking_History.objects.all().order_by('-booking_date')
    return render(request, 'admin/dashboard_bookings.html', {'bookings': bookings})

@login_required
def dashboard_services(request):
    if not request.user.is_admin: return redirect('home')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            name = request.POST.get('service_name')
            price = request.POST.get('price')
            duration = request.POST.get('duration_minutes')
            
            if Services.objects.filter(service_name__iexact=name).exists():
                messages.error(request, f'Service with name "{name}" already exists.')
            else:
                service_id = f"S-{Services.objects.count() + 1}"
                Services.objects.create(service_id=service_id, service_name=name, price=price, duration_minutes=duration)
                messages.success(request, 'Service added successfully.')
        elif action == 'delete':
            service_id = request.POST.get('service_id')
            Services.objects.filter(id=service_id).delete()
            messages.success(request, 'Service deleted.')
        return redirect('dashboard_services')
        
    services = Services.objects.all().order_by('-created_at')
    return render(request, 'admin/dashboard_services.html', {'services': services})

@login_required
def dashboard_parkings(request):
    if not request.user.is_admin: return redirect('home')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            slot = request.POST.get('slot_number')
            if Parking_Slots.objects.filter(slot_number__iexact=slot).exists():
                messages.error(request, f'Parking slot "{slot}" already exists.')
            else:
                Parking_Slots.objects.create(slot_number=slot)
                messages.success(request, 'Parking slot added.')
        elif action == 'delete':
            slot_id = request.POST.get('slot_id')
            Parking_Slots.objects.filter(id=slot_id).delete()
            messages.success(request, 'Parking slot deleted.')
        return redirect('dashboard_parkings')
        
    slots = Parking_Slots.objects.all().order_by('created_at')
    return render(request, 'admin/dashboard_parkings.html', {'slots': slots})
@login_required
def profile_view(request):
    customer = Customers.objects.filter(user=request.user).first()
    if request.method == 'POST':
        u = request.POST.get('username').strip().upper()
        e = request.POST.get('email')
        c = request.POST.get('contact')
        a = request.POST.get('address')
        p = request.POST.get('password')
        pay_pin = request.POST.get('payment_pin')
        
        # Check if username is changing and if new username exists
        if u != request.user.username and CustomUser.objects.filter(username=u).exists():
            messages.error(request, 'Username already exists.')
        else:
            request.user.username = u
            request.user.email = e
            if p:
                request.user.set_password(p)
            request.user.save()
            
            # Re-authenticate if password changed
            if p:
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, request.user)
            
            if customer:
                customer.customer_name = u
                customer.email = e
                customer.contact = c
                customer.address = a
                if pay_pin and len(pay_pin) == 4 and pay_pin.isdigit():
                    customer.payment_pin = pay_pin
                customer.save()
            else:
                # In case customer object doesn't exist for some reason
                if request.user.is_customer:
                    c_id = f"M-{Customers.objects.count() + 101}"
                    import random
                    pin_val = f"{random.randint(0, 9999):04d}"
                    if pay_pin and len(pay_pin) == 4 and pay_pin.isdigit():
                        pin_val = pay_pin
                    Customers.objects.create(user=request.user, customer_id=c_id, customer_name=u, email=e, contact=c, address=a, payment_pin=pin_val)
            
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
            
    return render(request, 'profile.html', {'customer': customer})
