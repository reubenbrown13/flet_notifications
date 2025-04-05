from typing import Any, Optional
from datetime import datetime
from flet.core.control import Control

class LocalNotifications(Control):

    def __init__(
        self,
        #
        # Control
        #
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            tooltip=tooltip,
            visible=visible,
            data=data,
        )

    def _get_control_name(self):
        return "flet_notifications"

    async def show_notification(self, id: int, title: str, body: str, payload: Optional[str] = None) -> bool:
        """
        Mostra una notifica locale con il titolo, il corpo e il payload specificati.
        
        Args:
            id: L'ID univoco della notifica.
            title: Il titolo della notifica.
            body: Il corpo della notifica.
            payload: Un payload opzionale che può essere utilizzato quando si tocca la notifica.
            
        Returns:
            True se la notifica è stata mostrata con successo, False altrimenti.
        """
        args = {
            "id": str(id),
            "title": title,
            "body": body,
        }
        if payload:
            args["payload"] = payload
            
        result = await self.invoke_method_async("show_notification", args)
        return result == "ok"
    
    async def schedule_notification(
        self, id: int, title: str, body: str, scheduled_date: datetime,
        payload: Optional[str] = None
    ) -> bool:
        """
        Programma una notifica locale per una data e ora specifiche.
        
        Args:
            id: L'ID univoco della notifica.
            title: Il titolo della notifica.
            body: Il corpo della notifica.
            scheduled_date: La data e l'ora in cui mostrare la notifica.
            payload: Un payload opzionale che può essere utilizzato quando si tocca la notifica.
            
        Returns:
            True se la notifica è stata programmata con successo, False altrimenti.
        """
        args = {
            "id": str(id),
            "title": title,
            "body": body,
            "scheduled_date": scheduled_date.isoformat(),
        }
        if payload:
            args["payload"] = payload
            
        result = await self.invoke_method_async("schedule_notification", args)
        return result == "ok"
    
    async def request_permissions(self) -> bool:
        """
        Richiede i permessi per le notifiche.
        
        Returns:
            True se i permessi sono stati concessi, False altrimenti.
        """
        result = await self.invoke_method_async("request_permissions", {})
        return result.lower() == "true"