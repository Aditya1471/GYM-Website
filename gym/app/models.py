from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Contact(models.Model):
    name= models.CharField(max_length= 200,null=True)
    email= models.EmailField()
    sub= models.CharField(max_length=200,null=True)
    message= models.CharField(max_length= 200,null=True)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    image=models.FileField(upload_to='product/',blank=True, null=True)
    image1=models.FileField(upload_to='product/',blank=True, null=True)
    image2=models.FileField(upload_to='product/',blank=True, null=True)
    image3=models.FileField(upload_to='product/',blank=True, null=True)
    name = models.CharField(max_length=100,null=False,blank=False)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE,default=False,null=True)
    description = models.TextField()
    percentage=models.CharField(max_length=100,null=True)
    dell=  models.SmallIntegerField(default=0,null=False,blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacture_date = models.CharField(max_length=100, default="October 2025", null=True, blank=True)
    expiry_date = models.CharField(max_length=100, default="October 2027", null=True, blank=True)
    manufacturer = models.TextField(default="Fit-Hit Nutrition Labs Inc., Plot 42, Industrial Area, Phase-1, Chandigarh, India", null=True, blank=True)
    highlights = models.TextField(null=True, blank=True, help_text="Separate with newlines")

    @property
    def get_highlights_list(self):
        if self.highlights:
            return [h.strip() for h in self.highlights.split('\n') if h.strip()]
        
        name_lower = self.name.lower()
        if "creatine" in name_lower:
            return [
                "<strong>HELPS BUILD MUSCLE & STRENGTH:</strong> Every scoop delivers the fuel for your physical performance. It helps you train harder, lift heavier, and recover faster.",
                "<strong>RECOVER FROM WORKOUTS FASTER:</strong> Get back into the gym faster and stronger. Wellcore creatine powder helps replenish energy, reduce fatigue, and promote muscle repair, making it essential for gym enthusiasts.",
                "<strong>PREMIUM QUALITY:</strong> With no artificial colours, no artificial flavors, no sugar & no fillers you can be rest assured that you’re choosing a high-quality creatine supplement to support your health & physical performance.",
                "<strong>CERTIFIED BY TRUSTIFIED:</strong> Wellcore creatine powder is a Trustified certified product, indicating that the product has the ingredients & effectiveness it claims."
            ]
        elif "protein" in name_lower or "whey" in name_lower:
            return [
                "<strong>ACCELERATED MUSCLE GROWTH:</strong> Rich in essential amino acids and BCAAs to feed muscle fibers and trigger rapid muscle protein synthesis.",
                "<strong>FAST-DIGESTING FORMULA:</strong> Absorbs rapidly post-workout to kickstart recovery and repair muscle micro-tears immediately.",
                "<strong>PREMIUM MACROS:</strong> Low fat, low sugar, and high protein yield per scoop for lean muscle mass conditioning.",
                "<strong>LAB TESTED & CERTIFIED:</strong> Guaranteed hormone-free and certified clean of banned substances for safe daily consumption."
            ]
        elif "pre" in name_lower or "workout" in name_lower:
            return [
                "<strong>EXPLOSIVE ENERGY & FOCUS:</strong> Formulated with beta-alanine and caffeine for clean, long-lasting energy without any crash.",
                "<strong>MAXIMUM MUSCLE PUMP:</strong> Enhances nitric oxide levels for skin-splitting pumps, active vascularity, and muscle cell volume.",
                "<strong>STAMINA & ENDURANCE:</strong> Buffers lactic acid buildup, letting you push through tough final reps with absolute power.",
                "<strong>CLEAN INGREDIENTS:</strong> No-crash formula with zero sugar, zero fillers, and lab-verified safety certifications."
            ]
        elif "fish" in name_lower or "omega" in name_lower:
            return [
                "<strong>JOINT COMFORT & RECOVERY:</strong> Lubricates heavy lifting joints, reducing friction, stiffness, and workout inflammation.",
                "<strong>HEART & BRAIN HEALTH:</strong> High concentration of EPA and DHA to support cognitive focus and cardiovascular efficiency.",
                "<strong>ZERO FISHY AFTERTASTE:</strong> Premium enteric-coated capsules to prevent reflux, ensuring easy absorption and digestion.",
                "<strong>PURITY VERIFIED:</strong> Molecularly distilled to be completely free of heavy metals, mercury, and PCB contaminants."
            ]
        else:
            return [
                "<strong>ENHANCED PHYSICAL PERFORMANCE:</strong> Carefully formulated to fuel your daily workouts and support overall physical stamina.",
                "<strong>OPTIMIZED RECOVERY KINETICS:</strong> Helps replenish depleted glycogen stores, reduce fatigue, and promote muscle tissue repair.",
                "<strong>PREMIUM QUALITY INGREDIENTS:</strong> Contains no artificial colors, no sugar, and zero fillers for clean dietary wellness.",
                "<strong>SAFETY CERTIFIED:</strong> Formulated in GMP-certified facilities to ensure premium quality control standards are met."
            ]

    def __str__(self):
        return self.name

    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Cart {self.id} - {self.user.username}"

class CartItem(models.Model):
    image=models.FileField(upload_to='cart/',blank=True, null=True)
    cart = models.ForeignKey(Cart, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=0)

    @property
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.user.username}"

STATE_CHOICES = (
('Himachal','Himachal'),
('Chandigarh','Chandigarh'),
('Punjab','Punjab'),
('Haryana', 'Haryana'),
('Delhi', 'Delhi'),
('Uttar Pradesh', 'Uttar Pradesh'),
('Rajasthan', 'Rajasthan'),
('Madhya Pradesh', 'Madhya Pradesh'),
('Gujarat', 'Gujarat'),
('Maharashtra', 'Maharashtra'),
('Karnataka', 'Karnataka'),
('Andhra Pradesh', 'Andhra Pradesh'),
('Telangana', 'Telangana'),
('Tamil Nadu', 'Tamil Nadu'),
('Kerala', 'Kerala'),
('Odisha', 'Odisha'),
('West Bengal', 'West Bengal'),
('Bihar', 'Bihar'),
('Jharkhand', 'Jharkhand'),
('Assam', 'Assam'),
('Meghalaya', 'Meghalaya'),
('Arunachal Pradesh', 'Arunachal Pradesh'),
('Sikkim', 'Sikkim'),
('Nagaland', 'Nagaland'),
('Mizoram', 'Mizoram'),
('Manipur', 'Manipur'),
('Tripura', 'Tripura'),
('Uttarakhand', 'Uttarakhand'),
)
class Customer(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	name = models.CharField(max_length = 200)
	locality = models.CharField(max_length= 200)
	city = models.CharField(max_length = 50)
	zipcode = models.IntegerField()
	state = models.CharField(choices = STATE_CHOICES, max_length = 50)
	phone = models.CharField(max_length = 15, blank = True, null = True)

	def __str__(self):
		return str(self.id)




