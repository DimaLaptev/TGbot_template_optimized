"""
Dependency Injection контейнер для управления зависимостями.
"""
from typing import Dict, Any, TypeVar, Type
from abc import ABC

T = TypeVar('T')


class DIContainer:
    """
    Простой DI контейнер для управления зависимостями.
    
    Реализует принцип Dependency Injection, позволяя
    регистрировать зависимости и получать их экземпляры.
    """
    
    def __init__(self) -> None:
        self._services: Dict[Type, Any] = {}
        self._singletons: Dict[Type, Any] = {}
    
    def register_singleton(self, interface: Type[T], implementation: T) -> None:
        """Зарегистрировать сервис как singleton."""
        self._singletons[interface] = implementation
    
    def register_transient(self, interface: Type[T], factory: callable) -> None:
        """Зарегистрировать сервис как transient (новый экземпляр каждый раз)."""
        self._services[interface] = factory
    
    def get(self, interface: Type[T]) -> T:
        """Получить экземпляр сервиса."""
        # Сначала проверяем singletons
        if interface in self._singletons:
            return self._singletons[interface]
        
        # Затем проверяем transient сервисы
        if interface in self._services:
            factory = self._services[interface]
            return factory()
        
        raise ValueError(f"Сервис {interface} не зарегистрирован")
    
    def has(self, interface: Type[T]) -> bool:
        """Проверить, зарегистрирован ли сервис."""
        return interface in self._singletons or interface in self._services


# Глобальный экземпляр контейнера
container = DIContainer() 