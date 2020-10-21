import requests
import bs4
import re
import cloudscraper


scraper = cloudscraper.create_scraper()


for x in range(1,297):
    print('Pagina {}'.format(x))
    response = scraper.get('https://www.zonaprop.com.ar/inmuebles-venta-lanus-pagina-{}.html'.format(x)).text
    html = bs4.BeautifulSoup(response,'html.parser')
    inmuebles = html.select('.posting-card')

    for inmueble in inmuebles:
        if inmueble.get('data-posting-type') != 'DEVELOPMENT':
            idzonap = inmueble.get('data-id')
            if len(inmueble.select('.first-price')) == 0:
                precio = 0
            else:
                precio = inmueble.select('.first-price')[0].text.replace('.','')[4:]
            caracteristicas = inmueble.select('li')
            m2 = 0
            m2cub = 0
            ambientes = 0
            banios = 0
            cocheras = 0
            for carac in caracteristicas:
                if carac.text.find('totales') >= 0:
                    m2 = int(re.findall('\d+', carac.text )[0])
                elif carac.text.find('cubiertos') >= 0:
                    m2cub = int(re.findall('\d+', carac.text )[0])
                elif carac.text.find('Ambiente') >= 0:
                    ambientes = int(re.findall('\d+', carac.text )[0])
                elif carac.text.find('Dormito') >= 0:
                    ambientes = int(re.findall('\d+', carac.text )[0])+1
                elif carac.text.find('Ba') >= 0:
                    banios = int(re.findall('\d+', carac.text )[0])
                elif carac.text.find('Cochera') >= 0:
                    cocheras = int(re.findall('\d+', carac.text )[0])

            if len(inmueble.select('.posting-location')[0].text.split(',')) == 2:
                direccion = ''
                localidad = inmueble.select('.posting-location')[0].text.split(',')[0].strip().replace('Lans','Lanus')
                partido = inmueble.select('.posting-location')[0].text.split(',')[1].strip().replace('Lans','Lanus')
            else:
                direccion = inmueble.select('.posting-location')[0].text.split(',')[0].strip()
                localidad = inmueble.select('.posting-location')[0].text.split(',')[1].strip().replace('Lans','Lanus')
                partido = inmueble.select('.posting-location')[0].text.split(',')[2].strip().replace('Lans','Lanus')

            inmu = str(idzonap)+','+str(precio)+','+str(m2)+','+str(m2cub)+','+str(ambientes)+','+str(banios)+','+str(cocheras)+','+direccion+','+localidad+','+partido+'\n'
            archivo.write(inmu)