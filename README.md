# Astracore Group

Sitio oficial de Astracore Group. Primera etapa enfocada exclusivamente en la marca matriz corporativa.

## Desarrollo local
- Doble clic en iniciar_local.command (Mac) o iniciar_local.bat (Windows).
- El sitio queda disponible en http://127.0.0.1:8000

## Subir cambios
- Doble clic en subir_a_github.command (Mac) o subir_a_github.bat (Windows).

## Despliegue
- Hosting: Render (auto-deploy desde main).
- DNS/CDN: Cloudflare.

## Consultas de contacto
- Las consultas quedan guardadas en la base de datos y se pueden revisar en `/admin/` con una cuenta superusuario.
- Para crear la primera cuenta local: `python manage.py createsuperuser`.
- En desarrollo, el email se imprime en la consola del servidor.
- En Render, configura `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `EMAIL_USE_SSL`, `DEFAULT_FROM_EMAIL` y `CONTACT_EMAIL`.
- Usa un remitente verificado con tu proveedor SMTP. Guarda las credenciales solo en variables de entorno, nunca en el repositorio.

## Alcance actual
- Solo secciones institucionales de Astracore Group.
- Sin publicación de otras divisiones, marcas o iniciativas en esta etapa.
- Contenido editable y arquitectura preparada para futuras expansiones.
