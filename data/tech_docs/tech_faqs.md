# FAQs - TECH

## 1. No puedo iniciar sesión en la plataforma, ¿qué verifico primero?
Verifica que tu usuario y contraseña sean correctos, completa el MFA y asegúrate de estar conectado a la VPN si es requerido. Si el problema persiste, intenta restablecer tu contraseña. En caso de bloqueo de cuenta por intentos fallidos, solicita desbloqueo a IT adjuntando el mensaje de error.

## 2. ¿Cómo restablezco mi contraseña de forma segura?
Utiliza la opción 'Olvidé mi contraseña' y sigue el flujo de verificación. Se te enviará un enlace temporal para crear una nueva clave que cumpla con la política de complejidad. Evita reutilizar contraseñas anteriores.

## 3. No puedo conectarme a la VPN, ¿qué pasos sigo?
Verifica tu conexión a internet, credenciales y que el cliente VPN esté actualizado. Reinicia el cliente y tu equipo. Si el problema continúa, puede tratarse de certificados vencidos o permisos, por lo que deberás abrir un ticket.

## 4. ¿Cómo solicito acceso a un sistema o repositorio?
Debes realizar la solicitud desde el portal de IT indicando el sistema y la justificación. La aprobación dependerá del manager y del equipo de seguridad. Una vez aprobada, se asignarán los permisos correspondientes.

## 5. Recibo un error 500 en la aplicación, ¿qué significa?
Un error 500 indica un problema en el servidor. Intenta nuevamente y, si persiste, reporta el incidente con hora, endpoint y pasos para reproducirlo. Esto permite al equipo técnico identificar la causa.

## 6. ¿Qué es MFA y por qué es obligatorio?
El MFA agrega una capa adicional de seguridad mediante un segundo factor (app o token). Reduce el riesgo de accesos no autorizados incluso si la contraseña se ve comprometida.

## 7. No veo mis permisos actualizados, ¿qué hago?
Puede haber un retraso en la sincronización. Espera unos minutos y vuelve a intentar. Si no se actualiza, contacta a IT con el detalle del acceso solicitado.

## 8. ¿Cómo reporto un incidente crítico?
Abre un ticket con prioridad alta, incluye evidencia (logs, capturas) y notifica al canal de incidentes. Esto activa el protocolo de respuesta rápida.

## 9. La aplicación está lenta, ¿cómo lo analizo?
Verifica tu conexión, revisa si hay incidentes reportados y prueba en otro navegador. Si el problema persiste, reporta con métricas (tiempos de carga, endpoints afectados).

## 10. No puedo acceder al repositorio Git, ¿qué reviso?
Verifica tus permisos, la configuración de claves SSH y el estado del servicio. Si cambiaste de equipo, puede requerir reconfiguración.

## 11. ¿Cómo se realiza un deploy seguro?
Mediante pipelines CI/CD con pruebas automatizadas, revisión de código y aprobaciones. Siempre debe existir plan de rollback.

## 12. ¿Qué hago si mi cuenta fue bloqueada?
Solicita desbloqueo a IT y revisa intentos fallidos. Se recomienda usar gestor de contraseñas.

## 13. ¿Cómo accedo a logs de la aplicación?
Dependiendo del rol, podrás verlos en la herramienta de observabilidad. Si no tienes acceso, solicita permisos.

## 14. ¿Qué hago ante un incidente de seguridad?
Escala inmediatamente al equipo de seguridad, evita modificar evidencia y documenta el incidente.

## 15. ¿Cómo funcionan los backups?
Se realizan de forma periódica y permiten restaurar información ante fallos.

## 16. ¿Qué es SSO?
Single Sign-On permite acceder a múltiples sistemas con una sola autenticación.

## 17. ¿Cómo verifico el estado de un servicio?
Consulta el dashboard de monitoreo o la página de estado.

## 18. ¿Qué hago si falla el pipeline?
Revisa logs, corrige errores y vuelve a ejecutar.

## 19. ¿Cómo se gestionan permisos temporales?
Se otorgan con expiración automática y deben renovarse si es necesario.

## 20. ¿Qué herramientas de observabilidad usamos?
Se utilizan dashboards para logs, métricas y alertas en tiempo real.

## 21. ¿Cómo actualizar dependencias?
Mediante procesos controlados y pruebas previas.

## 22. ¿Qué hago si un endpoint falla?
Revisa logs, reproduce el error y reporta.

## 23. ¿Cómo proteger credenciales?
Usa vault seguro y evita compartirlas.

## 24. ¿Qué es IaC?
Infraestructura como código para gestionar configuraciones.

## 25. ¿Cómo se auditan accesos?
Periódicamente mediante revisiones de seguridad.

## 26. ¿Qué hago si hay timeout?
Revisa latencia y dependencias externas.

## 27. ¿Cómo funciona el rollback?
Permite volver a una versión estable ante fallos.

## 28. ¿Cómo reporto bugs?
Mediante tickets con detalle técnico.

## 29. ¿Qué hacer ante SSL vencido?
Renovar certificado inmediatamente.

## 30. ¿Cómo mejorar performance?
Optimizar consultas y recursos.

## ¿Qué hago si el login funciona pero me redirige constantemente al inicio?
Este comportamiento suele estar relacionado con problemas de sesión o cookies. Primero, intenta borrar cookies y cache del navegador. Si utilizas SSO, puede haber un conflicto con el token de autenticación. También es importante verificar si el sistema está teniendo incidentes activos. Si el problema persiste, abre un ticket indicando navegador, sistema operativo y pasos realizados.

## La aplicación funciona pero algunas funcionalidades no cargan, ¿a qué se debe?
Esto puede deberse a problemas de permisos, errores en APIs o datos inconsistentes. Verifica si tienes los permisos adecuados para esa funcionalidad. También puede ser un problema temporal del backend. Revisa si hay errores en consola del navegador y repórtalos al equipo técnico.

## ¿Cómo sé si un problema es de mi conexión o del sistema?
Puedes probar accediendo desde otra red o dispositivo. Si el problema persiste, probablemente sea del sistema. También puedes verificar el estado de los servicios en el dashboard interno o consultar con otros usuarios si experimentan el mismo problema.

## ¿Qué hago si una actualización rompió una funcionalidad que antes funcionaba?
En este caso, es importante reportar el problema indicando la versión del sistema, funcionalidad afectada y pasos para reproducirlo. El equipo técnico puede necesitar hacer rollback o aplicar un fix rápido.

## ¿Cómo funciona el control de versiones en los sistemas internos?
Los sistemas utilizan repositorios versionados donde cada cambio queda registrado. Antes de cada despliegue se realizan pruebas y validaciones. Esto permite revertir cambios en caso de errores.

## ¿Qué hago si el sistema muestra datos inconsistentes?
Primero valida si los datos provienen de múltiples fuentes. Luego intenta refrescar la información. Si persiste, puede tratarse de un problema de sincronización entre servicios.

## ¿Cómo se gestionan los accesos temporales?
Los accesos temporales se otorgan con una fecha de expiración definida. Una vez vencido el plazo, el acceso se revoca automáticamente por seguridad.

## ¿Qué significa un error de timeout?
Indica que el sistema tardó demasiado en responder. Puede deberse a problemas de red, alta carga o dependencias externas. Reintentar suele resolverlo, pero si es frecuente debe escalarse.

## ¿Cómo puedo mejorar el rendimiento de la aplicación desde mi lado?
Puedes cerrar aplicaciones en segundo plano, usar una conexión estable y mantener actualizado tu navegador. En algunos casos, limpiar cache también mejora el rendimiento.

## ¿Qué hago si recibo errores intermitentes?
Los errores intermitentes suelen ser difíciles de diagnosticar. Es clave registrar el momento exacto, acciones realizadas y cualquier patrón detectado.


## ¿Qué hago si el sistema me desconecta automáticamente después de iniciar sesión?
Esto suele estar relacionado con expiración de sesión o problemas en el manejo de tokens. Puede deberse a configuraciones de seguridad, tiempo de inactividad o inconsistencias en el navegador. Se recomienda limpiar cookies, probar en modo incógnito y verificar si el problema ocurre en múltiples dispositivos. Si persiste, el equipo técnico deberá revisar logs de autenticación.

## ¿Cómo identificar si un error proviene del frontend o del backend?
Los errores de frontend suelen mostrarse visualmente (botones que no responden, elementos rotos), mientras que los errores backend suelen generar mensajes como error 500 o fallos en APIs. Revisar la consola del navegador puede dar pistas claras. Para un diagnóstico completo, es clave incluir logs y endpoints afectados.

## ¿Qué hacer si una funcionalidad tarda demasiado en responder?
Primero verificar si el problema es general o específico del usuario. Puede tratarse de latencia, consultas ineficientes o sobrecarga del sistema. Se recomienda medir tiempos de respuesta y revisar si hay incidentes activos.

## ¿Por qué una funcionalidad funciona para otros usuarios pero no para mí?
Esto generalmente indica un problema de permisos o configuración de usuario. Es importante verificar roles asignados, configuraciones específicas y diferencias entre usuarios.

## ¿Cómo manejar errores recurrentes que no se pueden reproducir fácilmente?
Registrar la mayor cantidad de información posible: hora, acción realizada, entorno y frecuencia. Este tipo de errores requiere análisis de logs históricos y monitoreo.

## ¿Qué implica un despliegue fallido y cómo afecta a los usuarios?
Un deploy fallido puede dejar funcionalidades inestables o no disponibles. En estos casos se suele aplicar rollback a la versión anterior para restaurar estabilidad.

## ¿Cómo saber si un problema es causado por una dependencia externa?
Si el sistema depende de APIs externas, cualquier falla en ellas impacta directamente. Se recomienda revisar logs y estado del proveedor externo.

## ¿Qué hacer si el sistema muestra información desactualizada?
Puede tratarse de cache o problemas de sincronización. Refrescar datos o invalidar cache suele resolverlo.

## ¿Cómo reportar correctamente un bug?
Debe incluir pasos para reproducirlo, comportamiento esperado vs actual, entorno (browser, OS) y evidencia (capturas o logs).

## ¿Qué hacer si el sistema presenta errores después de una actualización reciente?
Esto suele indicar regresiones. Se recomienda reportarlo rápidamente para evaluar rollback o fix urgente.