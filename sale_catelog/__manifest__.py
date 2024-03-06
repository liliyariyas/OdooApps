{
    'name': "Sale Catelog",
    'summary': "Sale Catelog",
    'description': """Sale Catelog""",
    'author': "Fathima Liliya",
    'category': 'Sale',
    'version': "16.0.1.0.0",
    'depends': ['sale','stock'],
    'data': [
        'views/product_product_views.xml',
        'views/sale.xml', 
    ],
    'assets': {
        'web.assets_backend': [
            'sale_catelog/static/src/components/**/*',
            'sale_catelog/static/src/views/**/*',
       
        ],
   
    },
    'demo': [],
    'qweb': [],
    'images': ['static/description/icon.png'],
    'license': 'OEEL-1',
    "auto_install": False,
    "application": False,    
}
