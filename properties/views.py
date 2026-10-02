from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Property, RentalRequest, Review
from .forms import PropertyForm, RentalRequestForm, ReviewForm

def property_list(request):
    properties = Property.objects.all().order_by('-created_at')
    
    # Simple search filter (if user searches by title or address)
    query = request.GET.get('q')
    if query:
        properties = properties.filter(title__icontains=query) | properties.filter(address__icontains=query)
        
    context = {
        'properties': properties,
    }
    return render(request, 'properties/property_list.html', context)

def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    rental_form = RentalRequestForm()
    review_form = ReviewForm()
    
    context = {
        'property': property_obj,
        'rental_form': rental_form,
        'review_form': review_form,
    }
    return render(request, 'properties/property_detail.html', context)

@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()
            messages.success(request, 'Property created successfully!')
            return redirect('property_detail', pk=property_obj.pk)
    else:
        form = PropertyForm()
    return render(request, 'properties/property_form.html', {'form': form, 'title': 'Add Property'})

@login_required
def property_update(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('property_detail', pk=property_obj.pk)
    else:
        form = PropertyForm(instance=property_obj)
    return render(request, 'properties/property_form.html', {'form': form, 'title': 'Edit Property'})

@login_required
def property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('property_list')
    return render(request, 'properties/property_confirm_delete.html', {'property': property_obj})

@login_required
def dashboard(request):
    user_properties = Property.objects.filter(owner=request.user)
    rental_requests = RentalRequest.objects.filter(tenant=request.user)
    context = {
        'user_properties': user_properties,
        'rental_requests': rental_requests,
    }
    return render(request, 'properties/dashboard.html', context)

@login_required
def rental_request_list(request):
    requests = RentalRequest.objects.filter(property__owner=request.user)
    return render(request, 'properties/rental_request_list.html', {'requests': requests})

@login_required
def update_request_status(request, pk):
    rental_req = get_object_or_404(RentalRequest, pk=pk, property__owner=request.user)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['Approved', 'Rejected']:
            rental_req.status = status
            rental_req.save()
            messages.success(request, f'Request status updated to {status}.')
    return redirect('rental_request_list')

@login_required
def send_request(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = RentalRequestForm(request.POST)
        if form.is_valid():
            rental_req = form.save(commit=False)
            rental_req.property = property_obj
            rental_req.tenant = request.user
            rental_req.save()
            messages.success(request, 'Rental request sent successfully!')
            return redirect('property_detail', pk=pk)
    return redirect('property_detail', pk=pk)