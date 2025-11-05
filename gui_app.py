#!/usr/bin/env python3
"""
Email Router GUI Application
ইমেইল রাউটার GUI অ্যাপ্লিকেশন

A beautiful graphical interface for managing email routing rules and settings.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import yaml
import json
import threading
import os
import time
from pathlib import Path
from datetime import datetime
import sys
import logging

# Import the email router
from email_router import EmailRouter

# Setup logger
logger = logging.getLogger(__name__)


class ModernGUI:
    """Modern GUI application for Email Router"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Email Router")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Variables
        self.router = None
        self.router_thread = None
        self.is_running = False
        self.config_path = 'config.yaml'
        self.rules_path = 'routing_rules.yaml'
        
        # Load configuration
        self.load_config()
        self.load_rules()
        
        # Setup UI
        self.setup_ui()
        
        # Start status monitoring
        self.update_status()
        
    def setup_ui(self):
        """Setup the user interface"""
        
        # Modern gradient color scheme
        self.colors = {
            'bg': '#f5f7fa',
            'bg_secondary': '#e8ecf1',
            'fg': '#2c3e50',
            'fg_light': '#5a6c7d',
            'primary': '#667eea',
            'primary_dark': '#5568d3',
            'primary_light': '#818cf8',
            'secondary': '#4facfe',
            'secondary_dark': '#00f2fe',
            'success': '#10b981',
            'success_dark': '#059669',
            'danger': '#ef4444',
            'danger_dark': '#dc2626',
            'warning': '#f59e0b',
            'warning_dark': '#d97706',
            'light_bg': '#ffffff',
            'card_bg': '#ffffff',
            'border': '#e5e7eb',
            'border_light': '#f3f4f6',
            'shadow': '#e5e7eb',
            'text_muted': '#6b7280',
            'accent': '#8b5cf6',
            'accent_light': '#a78bfa'
        }
        
        # Configure root style with modern look
        self.root.configure(bg=self.colors['bg'])
        
        # Configure ttk styles for modern look
        style = ttk.Style()
        style.theme_use('clam')
        
        # Modern button styles
        style.configure('Modern.TButton',
            font=('Segoe UI', 10, 'bold'),
            borderwidth=0,
            focuscolor='none',
            padding=10
        )
        
        # Modern frame styles
        style.configure('Card.TFrame', background=self.colors['card_bg'])
        style.configure('Modern.TNotebook', background=self.colors['bg'], borderwidth=0)
        style.configure('Modern.TNotebook.Tab',
            padding=[20, 12],
            font=('Segoe UI', 10, 'bold'),
            background=self.colors['bg_secondary'],
            foreground=self.colors['fg']
        )
        style.map('Modern.TNotebook.Tab',
            background=[('selected', self.colors['light_bg'])],
            expand=[('selected', [1, 1, 1, 0])]
        )
        
        # Create main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main_container)
        
        # Notebook for tabs with modern style
        self.notebook = ttk.Notebook(main_container, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_config_tab()
        self.create_rules_tab()
        self.create_logs_tab()
        
    def create_header(self, parent):
        """Create header with title and status"""
        # Modern gradient header
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=90)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Gradient effect with secondary frame
        gradient_frame = tk.Frame(header_frame, bg=self.colors['primary_dark'])
        gradient_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title with modern styling
        title_container = tk.Frame(gradient_frame, bg=self.colors['primary_dark'])
        title_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        title_label = tk.Label(
            title_container,
            text="📧 Email Router",
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['primary_dark'],
            fg='white'
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(
            title_container,
            text="Automated Email Routing System",
            font=('Segoe UI', 10),
            bg=self.colors['primary_dark'],
            fg='#e0e7ff'
        )
        subtitle_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Status indicator with modern design
        status_container = tk.Frame(gradient_frame, bg=self.colors['primary_dark'])
        status_container.pack(side=tk.RIGHT, padx=25, pady=20)
        
        # Status card
        status_card = tk.Frame(status_container, bg='#ffffff', relief=tk.FLAT, bd=0)
        status_card.pack(side=tk.LEFT, padx=(0, 15))
        
        self.status_indicator = tk.Label(
            status_card,
            text="●",
            font=('Segoe UI', 16),
            bg='#ffffff',
            fg=self.colors['danger'],
            padx=12,
            pady=8
        )
        self.status_indicator.pack(side=tk.LEFT)
        
        status_text_frame = tk.Frame(status_card, bg='#ffffff')
        status_text_frame.pack(side=tk.LEFT, padx=(0, 12), pady=8)
        
        self.status_label = tk.Label(
            status_text_frame,
            text="Stopped",
            font=('Segoe UI', 11, 'bold'),
            bg='#ffffff',
            fg=self.colors['fg']
        )
        self.status_label.pack(anchor=tk.W)
        
        # Modern control buttons
        control_frame = tk.Frame(status_container, bg=self.colors['primary_dark'])
        control_frame.pack(side=tk.LEFT)
        
        self.start_btn = tk.Button(
            control_frame,
            text="▶ Start",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['success'],
            fg='white',
            activebackground=self.colors['success_dark'],
            activeforeground='white',
            relief=tk.FLAT,
            borderwidth=0,
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.start_router
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(
            control_frame,
            text="⏸ Stop",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['danger'],
            fg='white',
            activebackground=self.colors['danger_dark'],
            activeforeground='white',
            relief=tk.FLAT,
            borderwidth=0,
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.stop_router,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
    def create_dashboard_tab(self):
        """Create dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Modern card-based statistics
        stats_container = tk.Frame(dashboard_frame, bg=self.colors['bg'])
        stats_container.pack(fill=tk.X, padx=20, pady=20)
        
        # Statistics cards
        stats_frame = tk.Frame(stats_container, bg=self.colors['card_bg'], relief=tk.FLAT, bd=0)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Card header with gradient effect
        card_header = tk.Frame(stats_frame, bg=self.colors['primary'], height=50)
        card_header.pack(fill=tk.X)
        card_header.pack_propagate(False)
        
        tk.Label(
            card_header,
            text="📊 Statistics",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        stats_inner = tk.Frame(stats_frame, bg=self.colors['card_bg'])
        stats_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Modern stat cards grid
        stats_grid = tk.Frame(stats_inner, bg=self.colors['card_bg'])
        stats_grid.pack(fill=tk.BOTH, expand=True)
        
        # Stat card 1: Total Rules
        self.total_rules_label = self.create_stat_card(stats_grid, "Total Rules", f"{len(self.rules_data.get('rules', []))}", self.colors['primary'], 0, 0)
        
        # Stat card 2: Enabled Rules
        enabled_count = sum(1 for r in self.rules_data.get('rules', []) if r.get('enabled', True))
        self.enabled_rules_label = self.create_stat_card(stats_grid, "Enabled Rules", f"{enabled_count}", self.colors['success'], 0, 1)
        
        # Stat card 3: Last Check
        stat_card3 = tk.Frame(stats_grid, bg=self.colors['card_bg'], relief=tk.FLAT, bd=1)
        stat_card3.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')
        tk.Label(stat_card3, text="Last Check", font=('Segoe UI', 10), bg=self.colors['card_bg'], fg=self.colors['text_muted']).pack(pady=(15, 5))
        self.last_check_label = tk.Label(stat_card3, text="Never", font=('Segoe UI', 20, 'bold'), bg=self.colors['card_bg'], fg=self.colors['secondary'])
        self.last_check_label.pack(pady=(0, 15))
        
        # Stat card 4: Failed Emails
        stat_card4 = tk.Frame(stats_grid, bg=self.colors['card_bg'], relief=tk.FLAT, bd=1)
        stat_card4.grid(row=0, column=3, padx=10, pady=10, sticky='nsew')
        tk.Label(stat_card4, text="Failed Emails", font=('Segoe UI', 10), bg=self.colors['card_bg'], fg=self.colors['text_muted']).pack(pady=(15, 5))
        self.failed_emails_label = tk.Label(stat_card4, text="0", font=('Segoe UI', 20, 'bold'), bg=self.colors['card_bg'], fg=self.colors['warning'])
        self.failed_emails_label.pack(pady=(0, 15))
        self.update_failed_count()
        
        stats_grid.columnconfigure(0, weight=1)
        stats_grid.columnconfigure(1, weight=1)
        stats_grid.columnconfigure(2, weight=1)
        stats_grid.columnconfigure(3, weight=1)
        
        # Quick actions with modern card design
        actions_frame = tk.Frame(dashboard_frame, bg=self.colors['card_bg'], relief=tk.FLAT, bd=0)
        actions_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Card header
        actions_header = tk.Frame(actions_frame, bg=self.colors['secondary'], height=50)
        actions_header.pack(fill=tk.X)
        actions_header.pack_propagate(False)
        
        tk.Label(
            actions_header,
            text="⚡ Quick Actions",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['secondary'],
            fg='white'
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        actions_inner = tk.Frame(actions_frame, bg=self.colors['card_bg'])
        actions_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Modern action buttons grid
        btn_container = tk.Frame(actions_inner, bg=self.colors['card_bg'])
        btn_container.pack(expand=True)
        
        # Button 1: Run Once
        self.create_modern_button(btn_container, "▶ Run Once", self.colors['secondary'], self.colors['secondary_dark'], self.run_once, 0, 0)
        
        # Button 2: View Logs
        self.create_modern_button(btn_container, "📋 View Logs", self.colors['primary'], self.colors['primary_dark'], lambda: self.notebook.select(3), 0, 1)
        
        # Button 3: Retry Failed
        self.create_modern_button(btn_container, "🔄 Retry Failed", self.colors['warning'], self.colors['warning_dark'], self.retry_failed_emails, 0, 2)
        
        # Button 4: Manage Rules
        self.create_modern_button(btn_container, "⚙️ Manage Rules", self.colors['accent'], self.colors['accent_light'], lambda: self.notebook.select(2), 0, 3)
        
    def create_config_tab(self):
        """Create configuration tab"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ Configuration")
        
        # Scrollable frame
        canvas = tk.Canvas(config_frame, bg=self.colors['bg'])
        scrollbar = ttk.Scrollbar(config_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Email settings section
        email_section = self.create_section(scrollable_frame, "Email Settings")
        
        # Email Provider Helper
        provider_helper_frame = tk.Frame(email_section, bg=self.colors['light_bg'])
        provider_helper_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            provider_helper_frame,
            text="Email Provider:",
            font=('Arial', 10),
            bg=self.colors['light_bg'],
            width=30,
            anchor=tk.W
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        provider_var = tk.StringVar(value='auto')
        provider_combo = ttk.Combobox(
            provider_helper_frame,
            textvariable=provider_var,
            values=['Auto Detect', 'Gmail', 'Outlook/Office365', 'Yahoo', 'Custom'],
            font=('Arial', 10),
            width=25,
            state='readonly'
        )
        provider_combo.pack(side=tk.LEFT, padx=5)
        
        # Auto-fill button
        def auto_fill_settings():
            email_addr = self.config_vars['email_address'].get().strip().lower()
            if not email_addr:
                messagebox.showwarning("Warning", "Please enter email address first!")
                return
            
            # Detect provider
            provider = 'custom'
            if '@gmail.com' in email_addr:
                provider = 'gmail'
            elif '@outlook.com' in email_addr or '@hotmail.com' in email_addr or '@office365.com' in email_addr or '@live.com' in email_addr:
                provider = 'outlook'
            elif '@yahoo.com' in email_addr or '@yahoo.co.uk' in email_addr:
                provider = 'yahoo'
            else:
                # Custom domain - try common patterns
                domain = email_addr.split('@')[1] if '@' in email_addr else ''
                provider = 'custom'
                if domain:
                    # Common patterns for custom domains
                    # Try: mail.domain.com first (most common)
                    imap_server = f"mail.{domain}"
                    smtp_server = f"mail.{domain}"
                    
                    # Alternative: imap.domain.com / smtp.domain.com
                    # User can manually change if needed
                    
                    self.config_vars['imap_server'].delete(0, tk.END)
                    self.config_vars['imap_server'].insert(0, imap_server)
                    self.config_vars['imap_port'].delete(0, tk.END)
                    self.config_vars['imap_port'].insert(0, '993')
                    self.config_vars['smtp_server'].delete(0, tk.END)
                    self.config_vars['smtp_server'].insert(0, smtp_server)
                    # Default to port 465 for custom domains (most common)
                    self.config_vars['smtp_port'].delete(0, tk.END)
                    self.config_vars['smtp_port'].insert(0, '465')
                    provider_var.set('Custom')
                    
                    messagebox.showinfo(
                        "Custom Domain",
                        f"Custom domain detected!\n\n"
                        f"Auto-filled settings:\n"
                        f"IMAP: mail.{domain} (Port: 993)\n"
                        f"SMTP: mail.{domain} (Port: 465 - SSL)\n\n"
                        f"Please verify these settings with your email provider.\n"
                        f"If different, please update manually.\n\n"
                        f"Common SMTP ports:\n"
                        f"- 465 (SSL/TLS - most common for custom domains)\n"
                        f"- 587 (STARTTLS)\n"
                        f"- 25 (plain, not recommended)"
                    )
                    return
            
            # Fill settings based on provider
            if provider == 'gmail':
                self.config_vars['imap_server'].delete(0, tk.END)
                self.config_vars['imap_server'].insert(0, 'imap.gmail.com')
                self.config_vars['imap_port'].delete(0, tk.END)
                self.config_vars['imap_port'].insert(0, '993')
                self.config_vars['smtp_server'].delete(0, tk.END)
                self.config_vars['smtp_server'].insert(0, 'smtp.gmail.com')
                self.config_vars['smtp_port'].delete(0, tk.END)
                self.config_vars['smtp_port'].insert(0, '587')
                provider_var.set('Gmail')
                messagebox.showinfo("Success", "Gmail settings auto-filled!\nGmail settings automatically filled!\n\nNote: Use App Password, not regular password.")
            elif provider == 'outlook':
                self.config_vars['imap_server'].delete(0, tk.END)
                self.config_vars['imap_server'].insert(0, 'outlook.office365.com')
                self.config_vars['imap_port'].delete(0, tk.END)
                self.config_vars['imap_port'].insert(0, '993')
                self.config_vars['smtp_server'].delete(0, tk.END)
                self.config_vars['smtp_server'].insert(0, 'smtp.office365.com')
                self.config_vars['smtp_port'].delete(0, tk.END)
                self.config_vars['smtp_port'].insert(0, '587')
                provider_var.set('Outlook/Office365')
                messagebox.showinfo("Success", "Outlook/Office365 settings auto-filled!")
            elif provider == 'yahoo':
                self.config_vars['imap_server'].delete(0, tk.END)
                self.config_vars['imap_server'].insert(0, 'imap.mail.yahoo.com')
                self.config_vars['imap_port'].delete(0, tk.END)
                self.config_vars['imap_port'].insert(0, '993')
                self.config_vars['smtp_server'].delete(0, tk.END)
                self.config_vars['smtp_server'].insert(0, 'smtp.mail.yahoo.com')
                self.config_vars['smtp_port'].delete(0, tk.END)
                self.config_vars['smtp_port'].insert(0, '587')
                provider_var.set('Yahoo')
                messagebox.showinfo("Success", "Yahoo settings auto-filled!\nNote: Yahoo requires App Password.")
        
        auto_fill_btn = tk.Button(
            provider_helper_frame,
            text="🔧 Auto-Fill Settings",
            font=('Arial', 9),
            bg=self.colors['secondary'],
            fg='white',
            relief=tk.FLAT,
            padx=10,
            pady=3,
            cursor='hand2',
            command=auto_fill_settings
        )
        auto_fill_btn.pack(side=tk.LEFT, padx=5)
        
        # Email address
        email_frame = tk.Frame(email_section, bg=self.colors['light_bg'])
        email_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            email_frame,
            text="Email Address:",
            font=('Arial', 10),
            bg=self.colors['light_bg'],
            width=30,
            anchor=tk.W
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        email_entry = tk.Entry(
            email_frame,
            font=('Arial', 10),
            bg='white',
            relief=tk.SOLID,
            bd=1
        )
        email_entry.insert(0, self.config.get('email', {}).get('address', ''))
        email_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Bind Enter key to auto-fill (optional)
        email_entry.bind('<Return>', lambda e: auto_fill_settings())
        
        # Store reference
        if not hasattr(self, 'config_vars'):
            self.config_vars = {}
        self.config_vars['email_address'] = email_entry
        
        # Helper text for email address
        email_helper = tk.Label(
            email_section,
            text="💡 Supports Gmail, Outlook, Yahoo, or custom domain emails (e.g., rony@epagebd.com)",
            font=('Arial', 9),
            bg=self.colors['light_bg'],
            fg=self.colors['primary'],
            wraplength=600,
            justify=tk.LEFT
        )
        email_helper.pack(anchor=tk.W, padx=20, pady=(0, 10))
        
        # Password with helper
        password_frame = tk.Frame(email_section, bg=self.colors['light_bg'])
        password_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            password_frame,
            text="Password (App Password):",
            font=('Arial', 10),
            bg=self.colors['light_bg'],
            width=30,
            anchor=tk.W
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        password_entry_frame = tk.Frame(password_frame, bg=self.colors['light_bg'])
        password_entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        password_entry = tk.Entry(
            password_entry_frame,
            font=('Arial', 10),
            bg='white',
            relief=tk.SOLID,
            bd=1,
            show='*'
        )
        password_entry.insert(0, self.config.get('email', {}).get('password', ''))
        password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Auto-format button to remove spaces
        def format_password():
            current = password_entry.get()
            # Remove all spaces
            formatted = current.replace(' ', '')
            password_entry.delete(0, tk.END)
            password_entry.insert(0, formatted)
        
        format_btn = tk.Button(
            password_entry_frame,
            text="🔧 Remove Spaces / ফাঁকা সরান",
            font=('Arial', 8),
            bg=self.colors['secondary'],
            fg='white',
            relief=tk.FLAT,
            padx=8,
            pady=2,
            cursor='hand2',
            command=format_password
        )
        format_btn.pack(side=tk.LEFT, padx=5)
        
        # Helper text below password field
        helper_text = tk.Label(
            email_section,
            text="💡 Gmail App Password: You can enter with or without spaces. Spaces will be automatically removed when saving.\n   (Example: 'abcd efgh ijkl mnop' → 'abcdefghijklmnop')",
            font=('Arial', 9),
            bg=self.colors['light_bg'],
            fg=self.colors['primary'],
            wraplength=600,
            justify=tk.LEFT
        )
        helper_text.pack(anchor=tk.W, padx=20, pady=(0, 10))
        
        # Store reference
        if not hasattr(self, 'config_vars'):
            self.config_vars = {}
        self.config_vars['email_password'] = password_entry
        
        # IMAP Server
        self.create_labeled_entry(
            email_section,
            "IMAP Server:",
            'imap_server',
            self.config.get('email', {}).get('imap_server', 'imap.gmail.com')
        )
        
        # IMAP Port
        self.create_labeled_entry(
            email_section,
            "IMAP Port:",
            'imap_port',
            str(self.config.get('email', {}).get('imap_port', 993))
        )
        
        # SMTP Server
        self.create_labeled_entry(
            email_section,
            "SMTP Server:",
            'smtp_server',
            self.config.get('email', {}).get('smtp_server', 'smtp.gmail.com')
        )
        
        # SMTP Port
        self.create_labeled_entry(
            email_section,
            "SMTP Port:",
            'smtp_port',
            str(self.config.get('email', {}).get('smtp_port', 587))
        )
        
        # SMTP Port helper text
        smtp_port_helper = tk.Label(
            email_section,
            text="💡 Port 465 = SSL/TLS (most custom domains), Port 587 = STARTTLS (Gmail/Outlook)",
            font=('Segoe UI', 9),
            bg=self.colors['light_bg'],
            fg=self.colors['text_muted'],
            wraplength=600,
            justify=tk.LEFT
        )
        smtp_port_helper.pack(anchor=tk.W, padx=20, pady=(0, 10))
        
        # Commercial Department section
        comm_section = self.create_section(scrollable_frame, "Commercial Department")
        
        tk.Label(
            comm_section,
            text="Email Addresses (one per line):",
            font=('Arial', 10),
            bg=self.colors['light_bg']
        ).pack(anchor=tk.W, pady=(10, 5))
        
        comm_text = '\n'.join(self.config.get('commercial_department', {}).get('emails', []))
        self.commercial_emails_text = tk.Text(
            comm_section,
            height=5,
            font=('Arial', 10),
            bg='white',
            relief=tk.SOLID,
            bd=1
        )
        self.commercial_emails_text.pack(fill=tk.X, padx=10, pady=5)
        self.commercial_emails_text.insert('1.0', comm_text)
        
        # Accounts Department section
        accounts_section = self.create_section(scrollable_frame, "Accounts Department")
        
        self.create_labeled_entry(
            accounts_section,
            "Email Address:",
            'accounts_email',
            self.config.get('accounts_department', {}).get('email', '')
        )
        
        # Processing Options section
        options_section = self.create_section(scrollable_frame, "Processing Options")
        
        self.mark_as_read_var = tk.BooleanVar(value=self.config.get('mark_as_read', True))
        tk.Checkbutton(
            options_section,
            text="Mark processed emails as read",
            variable=self.mark_as_read_var,
            font=('Arial', 10),
            bg=self.colors['light_bg']
        ).pack(anchor=tk.W, pady=5, padx=10)
        
        self.mark_unmatched_var = tk.BooleanVar(value=self.config.get('mark_unmatched_as_read', False))
        tk.Checkbutton(
            options_section,
            text="Mark unmatched emails as read",
            variable=self.mark_unmatched_var,
            font=('Arial', 10),
            bg=self.colors['light_bg']
        ).pack(anchor=tk.W, pady=5, padx=10)
        
        # Check interval
        self.create_labeled_entry(
            options_section,
            "Check Interval (seconds):",
            'check_interval',
            str(self.config.get('check_interval', 60))
        )
        
        # Save button
        save_btn = tk.Button(
            scrollable_frame,
            text="💾 Save Configuration",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['success'],
            fg='white',
            activebackground=self.colors['success_dark'],
            activeforeground='white',
            relief=tk.FLAT,
            borderwidth=0,
            padx=30,
            pady=15,
            cursor='hand2',
            command=self.save_config
        )
        save_btn.pack(pady=25)
        
    def create_rules_tab(self):
        """Create rules management tab"""
        rules_frame = ttk.Frame(self.notebook)
        self.notebook.add(rules_frame, text="📋 Rules")
        
        # Top frame with buttons
        top_frame = tk.Frame(rules_frame, bg=self.colors['bg'])
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            top_frame,
            text="➕ Add Rule",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['success'],
            fg='white',
            activebackground=self.colors['success_dark'],
            activeforeground='white',
            relief=tk.FLAT,
            borderwidth=0,
            padx=18,
            pady=8,
            cursor='hand2',
            command=self.add_rule_dialog
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            top_frame,
            text="🔄 Refresh",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            activebackground=self.colors['secondary_dark'],
            activeforeground='white',
            relief=tk.FLAT,
            borderwidth=0,
            padx=18,
            pady=8,
            cursor='hand2',
            command=self.refresh_rules
        ).pack(side=tk.LEFT, padx=5)
        
        # Rules list frame
        list_frame = tk.Frame(rules_frame, bg=self.colors['bg'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for rules
        columns = ('name', 'status', 'match_type', 'forward_to')
        self.rules_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        self.rules_tree.heading('name', text='Rule Name')
        self.rules_tree.heading('status', text='Status')
        self.rules_tree.heading('match_type', text='Match Type')
        self.rules_tree.heading('forward_to', text='Forward To')
        
        self.rules_tree.column('name', width=200)
        self.rules_tree.column('status', width=100)
        self.rules_tree.column('match_type', width=100)
        self.rules_tree.column('forward_to', width=400)
        
        scrollbar_rules = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.rules_tree.yview)
        self.rules_tree.configure(yscrollcommand=scrollbar_rules.set)
        
        self.rules_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_rules.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons frame
        action_frame = tk.Frame(rules_frame, bg=self.colors['bg'])
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            action_frame,
            text="✏️ Edit",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            activebackground=self.colors['secondary_dark'],
            activeforeground='white',
            relief=tk.FLAT,
            borderwidth=0,
            padx=18,
            pady=8,
            cursor='hand2',
            command=self.edit_rule
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            action_frame,
            text="🔄 Toggle",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['warning'],
            fg='white',
            activebackground=self.colors['warning_dark'],
            activeforeground='white',
            relief=tk.FLAT,
            borderwidth=0,
            padx=18,
            pady=8,
            cursor='hand2',
            command=self.toggle_rule
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            action_frame,
            text="🗑️ Delete",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['danger'],
            fg='white',
            activebackground=self.colors['danger_dark'],
            activeforeground='white',
            relief=tk.FLAT,
            borderwidth=0,
            padx=18,
            pady=8,
            cursor='hand2',
            command=self.delete_rule
        ).pack(side=tk.LEFT, padx=5)
        
        # Load rules into tree
        self.refresh_rules()
        
    def create_logs_tab(self):
        """Create logs viewer tab"""
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="📄 Logs")
        
        # Top frame with refresh button
        top_frame = tk.Frame(logs_frame, bg=self.colors['bg'])
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            top_frame,
            text="🔄 Refresh",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            activebackground=self.colors['secondary_dark'],
            activeforeground='white',
            relief=tk.FLAT,
            borderwidth=0,
            padx=18,
            pady=8,
            cursor='hand2',
            command=self.refresh_logs
        ).pack(side=tk.LEFT, padx=5)
        
        # Logs text area
        self.logs_text = scrolledtext.ScrolledText(
            logs_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='white'
        )
        self.logs_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load initial logs
        self.refresh_logs()
        
    def create_stat_card(self, parent, title, value, color, row, col):
        """Create a modern stat card"""
        card = tk.Frame(parent, bg=self.colors['card_bg'], relief=tk.FLAT, bd=1)
        card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        tk.Label(card, text=title, font=('Segoe UI', 10), bg=self.colors['card_bg'], fg=self.colors['text_muted']).pack(pady=(15, 5))
        label = tk.Label(card, text=value, font=('Segoe UI', 20, 'bold'), bg=self.colors['card_bg'], fg=color)
        label.pack(pady=(0, 15))
        
        return label
    
    def create_modern_button(self, parent, text, bg_color, active_color, command, row, col):
        """Create a modern styled button"""
        btn = tk.Button(
            parent,
            text=text,
            font=('Segoe UI', 10, 'bold'),
            bg=bg_color,
            fg='white',
            activebackground=active_color,
            activeforeground='white',
            relief=tk.FLAT,
            borderwidth=0,
            padx=20,
            pady=12,
            cursor='hand2',
            command=command
        )
        btn.grid(row=row, column=col, padx=8, pady=8, sticky='ew')
        parent.columnconfigure(col, weight=1)
        return btn
    
    def create_section(self, parent, title):
        """Create a modern section frame with title"""
        section = tk.Frame(parent, bg=self.colors['card_bg'], relief=tk.FLAT, bd=0)
        section.pack(fill=tk.X, padx=20, pady=15)
        
        # Section header with accent
        header = tk.Frame(section, bg=self.colors['primary'], height=45)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=title,
            font=('Segoe UI', 13, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT, padx=20, pady=12)
        
        return section
        
    def create_labeled_entry(self, parent, label_text, var_name, default_value, show=None):
        """Create a labeled entry field"""
        frame = tk.Frame(parent, bg=self.colors['light_bg'])
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            frame,
            text=label_text,
            font=('Segoe UI', 10),
            bg=self.colors['light_bg'],
            width=30,
            anchor=tk.W
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        entry = tk.Entry(
            frame,
            font=('Segoe UI', 10),
            bg='white',
            relief=tk.FLAT,
            bd=1,
            show=show
        )
        entry.insert(0, default_value)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Store reference
        if not hasattr(self, 'config_vars'):
            self.config_vars = {}
        self.config_vars[var_name] = entry
        
        return entry
        
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f) or {}
            else:
                self.config = {}
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load config: {e}")
            self.config = {}
            
    def load_rules(self):
        """Load rules from file"""
        try:
            if os.path.exists(self.rules_path):
                with open(self.rules_path, 'r', encoding='utf-8') as f:
                    self.rules_data = yaml.safe_load(f) or {'rules': []}
            else:
                self.rules_data = {'rules': []}
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load rules: {e}")
            self.rules_data = {'rules': []}
            
    def save_config(self):
        """Save configuration to file"""
        try:
            # Get password and remove spaces (Gmail App Password works with or without spaces)
            password = self.config_vars['email_password'].get().replace(' ', '')
            
            config = {
                'email': {
                    'address': self.config_vars['email_address'].get(),
                    'password': password,
                    'imap_server': self.config_vars['imap_server'].get(),
                    'imap_port': int(self.config_vars['imap_port'].get() or 993),
                    'smtp_server': self.config_vars['smtp_server'].get(),
                    'smtp_port': int(self.config_vars['smtp_port'].get() or 587)
                },
                'commercial_department': {
                    'emails': [e.strip() for e in self.commercial_emails_text.get('1.0', tk.END).strip().split('\n') if e.strip()]
                },
                'accounts_department': {
                    'email': self.config_vars['accounts_email'].get()
                },
                'mark_as_read': self.mark_as_read_var.get(),
                'mark_unmatched_as_read': self.mark_unmatched_var.get(),
                'check_interval': int(self.config_vars['check_interval'].get() or 60),
                'routing_rules_file': self.rules_path
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
            
            self.config = config
            messagebox.showinfo("Success", "Configuration saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")
            
    def refresh_rules(self):
        """Refresh rules list"""
        self.load_rules()
        
        # Clear tree
        for item in self.rules_tree.get_children():
            self.rules_tree.delete(item)
        
        # Add rules
        for rule in self.rules_data.get('rules', []):
            status = "✓ Enabled" if rule.get('enabled', True) else "✗ Disabled"
            forward_to = ', '.join(rule.get('forward_to', []))
            self.rules_tree.insert('', tk.END, values=(
                rule.get('name', 'Unnamed'),
                status,
                rule.get('match_type', 'any'),
                forward_to
            ))
        
        # Update dashboard stats
        if hasattr(self, 'total_rules_label'):
            enabled_count = sum(1 for r in self.rules_data.get('rules', []) if r.get('enabled', True))
            self.total_rules_label.config(text=str(len(self.rules_data.get('rules', []))))
            self.enabled_rules_label.config(text=str(enabled_count))
            
    def add_rule_dialog(self):
        """Open add rule dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Rule")
        dialog.geometry("650x850")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create notebook for tabs (Quick Rule and Advanced Rule)
        rule_notebook = ttk.Notebook(dialog)
        rule_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Quick Rule Tab
        quick_frame = tk.Frame(rule_notebook, bg=self.colors['bg'])
        rule_notebook.add(quick_frame, text="Quick Rule")
        
        # Quick Rule Instructions
        quick_info = tk.Label(
            quick_frame,
            text="All emails from a specific Commercial Department email will be forwarded to a specific Insurance Department email",
            font=('Arial', 10, 'italic'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            wraplength=550,
            justify=tk.LEFT
        )
        quick_info.pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        # Commercial Department Email Selection
        tk.Label(
            quick_frame,
            text="Commercial Department Email:",
            font=('Arial', 10, 'bold'),
            bg=self.colors['bg']
        ).pack(anchor=tk.W, padx=20, pady=(10, 5))
        
        commercial_emails = self.config.get('commercial_department', {}).get('emails', [])
        commercial_var = tk.StringVar()
        commercial_combo = ttk.Combobox(
            quick_frame,
            textvariable=commercial_var,
            values=commercial_emails,
            font=('Arial', 10),
            width=50,
            state='readonly' if commercial_emails else 'normal'
        )
        commercial_combo.pack(padx=20, pady=5, fill=tk.X)
        
        # Initialize commercial_entry for manual entry (if no emails in config)
        commercial_entry = None
        if not commercial_emails:
            tk.Label(
                quick_frame,
                text="⚠️ Please add Commercial Department emails in Configuration",
                font=('Arial', 9),
                bg=self.colors['bg'],
                fg=self.colors['warning']
            ).pack(anchor=tk.W, padx=20, pady=5)
            commercial_entry = tk.Entry(quick_frame, font=('Arial', 10), width=50)
            commercial_entry.pack(padx=20, pady=5, fill=tk.X)
        else:
            commercial_combo.current(0) if commercial_emails else None
        
        # Insurance Department Email
        tk.Label(
            quick_frame,
            text="Insurance Department Email:",
            font=('Arial', 10, 'bold'),
            bg=self.colors['bg']
        ).pack(anchor=tk.W, padx=20, pady=(20, 5))
        
        insurance_entry = tk.Entry(quick_frame, font=('Arial', 10), width=50)
        insurance_entry.pack(padx=20, pady=5, fill=tk.X)
        
        # Rule Name for Quick Rule
        tk.Label(
            quick_frame,
            text="Rule Name (optional):",
            font=('Arial', 10),
            bg=self.colors['bg']
        ).pack(anchor=tk.W, padx=20, pady=(20, 5))
        
        quick_name_entry = tk.Entry(quick_frame, font=('Arial', 10), width=50)
        quick_name_entry.pack(padx=20, pady=5, fill=tk.X)
        
        # Enabled checkbox
        quick_enabled_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            quick_frame,
            text="Enabled",
            variable=quick_enabled_var,
            font=('Arial', 10),
            bg=self.colors['bg']
        ).pack(anchor=tk.W, padx=20, pady=10)
        
        def save_quick_rule():
            # Get commercial email
            if commercial_emails:
                commercial_email = commercial_var.get().strip()
            else:
                if commercial_entry:
                    commercial_email = commercial_entry.get().strip()
                else:
                    commercial_email = commercial_combo.get().strip()
            
            insurance_email = insurance_entry.get().strip()
            
            if not commercial_email:
                messagebox.showerror("Error", "Commercial Department email is required!")
                return
            
            if not insurance_email:
                messagebox.showerror("Error", "Insurance Department email is required!")
                return
            
            # Auto-generate rule name if not provided
            rule_name = quick_name_entry.get().strip()
            if not rule_name:
                rule_name = f"From {commercial_email} to {insurance_email}"
            
            rule = {
                'name': rule_name,
                'enabled': quick_enabled_var.get(),
                'match_type': 'any',
                'conditions': {
                    'from_contains': [commercial_email]
                },
                'forward_to': [insurance_email]
            }
            
            # Add to rules
            if 'rules' not in self.rules_data:
                self.rules_data['rules'] = []
            self.rules_data['rules'].append(rule)
            
            # Save to file
            try:
                with open(self.rules_path, 'w', encoding='utf-8') as f:
                    yaml.dump(self.rules_data, f, allow_unicode=True, default_flow_style=False)
                messagebox.showinfo("Success", "Quick rule added successfully!")
                dialog.destroy()
                self.refresh_rules()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save rule: {e}")
        
        # Save button for quick rule
        tk.Button(
            quick_frame,
            text="💾 Save Quick Rule",
            font=('Arial', 11, 'bold'),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2',
            command=save_quick_rule
        ).pack(pady=20)
        
        # Advanced Rule Tab
        advanced_frame = tk.Frame(rule_notebook, bg=self.colors['bg'])
        rule_notebook.add(advanced_frame, text="Advanced Rule")
        
        # Rule name
        tk.Label(advanced_frame, text="Rule Name:", font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=20, pady=(20, 5))
        name_entry = tk.Entry(advanced_frame, font=('Arial', 10), width=50)
        name_entry.pack(padx=20, pady=5)
        
        # Enabled
        enabled_var = tk.BooleanVar(value=True)
        tk.Checkbutton(advanced_frame, text="Enabled", variable=enabled_var, font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=20, pady=5)
        
        # Match type
        tk.Label(advanced_frame, text="Match Type:", font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=20, pady=(10, 5))
        match_type_var = tk.StringVar(value='any')
        tk.Radiobutton(advanced_frame, text="Any", variable=match_type_var, value='any', font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=40)
        tk.Radiobutton(advanced_frame, text="All", variable=match_type_var, value='all', font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=40)
        
        # Conditions
        tk.Label(advanced_frame, text="Subject Keywords (comma separated):", font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=20, pady=(10, 5))
        subject_entry = tk.Entry(advanced_frame, font=('Segoe UI', 10), width=50)
        subject_entry.pack(padx=20, pady=5)
        
        tk.Label(advanced_frame, text="Body Keywords (comma separated):", font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=20, pady=(10, 5))
        body_entry = tk.Entry(advanced_frame, font=('Segoe UI', 10), width=50)
        body_entry.pack(padx=20, pady=5)
        
        tk.Label(advanced_frame, text="From Contains (comma separated):", font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=20, pady=(10, 5))
        from_entry = tk.Entry(advanced_frame, font=('Segoe UI', 10), width=50)
        from_entry.pack(padx=20, pady=5)
        
        tk.Label(advanced_frame, text="Subject Regex (optional):", font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=20, pady=(10, 5))
        regex_entry = tk.Entry(advanced_frame, font=('Segoe UI', 10), width=50)
        regex_entry.pack(padx=20, pady=5)
        
        # Forward to
        tk.Label(advanced_frame, text="Forward To (one per line):", font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=20, pady=(10, 5))
        forward_text = tk.Text(advanced_frame, font=('Arial', 10), height=5, width=50)
        forward_text.pack(padx=20, pady=5)
        
        def save_rule():
            rule = {
                'name': name_entry.get().strip(),
                'enabled': enabled_var.get(),
                'match_type': match_type_var.get(),
                'conditions': {},
                'forward_to': [e.strip() for e in forward_text.get('1.0', tk.END).strip().split('\n') if e.strip()]
            }
            
            if not rule['name']:
                messagebox.showerror("Error", "Rule name is required!")
                return
                
            if not rule['forward_to']:
                messagebox.showerror("Error", "At least one forward address is required!")
                return
            
            conditions = {}
            if subject_entry.get().strip():
                conditions['subject_keywords'] = [k.strip() for k in subject_entry.get().split(',') if k.strip()]
            if body_entry.get().strip():
                conditions['body_keywords'] = [k.strip() for k in body_entry.get().split(',') if k.strip()]
            if from_entry.get().strip():
                conditions['from_contains'] = [f.strip() for f in from_entry.get().split(',') if f.strip()]
            if regex_entry.get().strip():
                conditions['subject_regex'] = regex_entry.get().strip()
            
            if not conditions:
                messagebox.showerror("Error", "At least one condition is required!")
                return
            
            rule['conditions'] = conditions
            
            # Add to rules
            if 'rules' not in self.rules_data:
                self.rules_data['rules'] = []
            self.rules_data['rules'].append(rule)
            
            # Save to file
            try:
                with open(self.rules_path, 'w', encoding='utf-8') as f:
                    yaml.dump(self.rules_data, f, allow_unicode=True, default_flow_style=False)
                messagebox.showinfo("Success", "Rule added successfully!")
                dialog.destroy()
                self.refresh_rules()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save rule: {e}")
        
        tk.Button(
            dialog,
            text="💾 Save",
            font=('Arial', 11, 'bold'),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2',
            command=save_rule
        ).pack(pady=20)
        
    def edit_rule(self):
        """Edit selected rule"""
        selection = self.rules_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a rule to edit")
            return
        
        item = self.rules_tree.item(selection[0])
        rule_name = item['values'][0]
        
        # Find rule
        rule = None
        rule_index = None
        for i, r in enumerate(self.rules_data.get('rules', [])):
            if r.get('name') == rule_name:
                rule = r
                rule_index = i
                break
        
        if not rule:
            messagebox.showerror("Error", "Rule not found")
            return
        
        # Open edit dialog (similar to add dialog but pre-filled)
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Rule")
        dialog.geometry("600x700")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Pre-fill form
        tk.Label(dialog, text="Rule Name:", font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=20, pady=(20, 5))
        name_entry = tk.Entry(dialog, font=('Arial', 10), width=50)
        name_entry.insert(0, rule.get('name', ''))
        name_entry.pack(padx=20, pady=5)
        
        enabled_var = tk.BooleanVar(value=rule.get('enabled', True))
        tk.Checkbutton(dialog, text="Enabled", variable=enabled_var, font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=20, pady=5)
        
        match_type_var = tk.StringVar(value=rule.get('match_type', 'any'))
        tk.Label(dialog, text="Match Type:", font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=20, pady=(10, 5))
        tk.Radiobutton(dialog, text="Any", variable=match_type_var, value='any', font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=40)
        tk.Radiobutton(dialog, text="All", variable=match_type_var, value='all', font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=40)
        
        conditions = rule.get('conditions', {})
        
        tk.Label(dialog, text="Subject Keywords:", font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=20, pady=(10, 5))
        subject_entry = tk.Entry(dialog, font=('Segoe UI', 10), width=50)
        subject_entry.insert(0, ', '.join(conditions.get('subject_keywords', [])))
        subject_entry.pack(padx=20, pady=5)
        
        tk.Label(dialog, text="Body Keywords:", font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=20, pady=(10, 5))
        body_entry = tk.Entry(dialog, font=('Segoe UI', 10), width=50)
        body_entry.insert(0, ', '.join(conditions.get('body_keywords', [])))
        body_entry.pack(padx=20, pady=5)
        
        tk.Label(dialog, text="From Contains:", font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=20, pady=(10, 5))
        from_entry = tk.Entry(dialog, font=('Segoe UI', 10), width=50)
        from_entry.insert(0, ', '.join(conditions.get('from_contains', [])))
        from_entry.pack(padx=20, pady=5)
        
        tk.Label(dialog, text="Subject Regex:", font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=20, pady=(10, 5))
        regex_entry = tk.Entry(dialog, font=('Segoe UI', 10), width=50)
        regex_entry.insert(0, conditions.get('subject_regex', ''))
        regex_entry.pack(padx=20, pady=5)
        
        tk.Label(dialog, text="Forward To (one per line):", font=('Segoe UI', 10), bg=self.colors['bg']).pack(anchor=tk.W, padx=20, pady=(10, 5))
        forward_text = tk.Text(dialog, font=('Segoe UI', 10), height=5, width=50)
        forward_text.insert('1.0', '\n'.join(rule.get('forward_to', [])))
        forward_text.pack(padx=20, pady=5)
        
        def save_rule():
            rule['name'] = name_entry.get().strip()
            rule['enabled'] = enabled_var.get()
            rule['match_type'] = match_type_var.get()
            rule['forward_to'] = [e.strip() for e in forward_text.get('1.0', tk.END).strip().split('\n') if e.strip()]
            
            conditions = {}
            if subject_entry.get().strip():
                conditions['subject_keywords'] = [k.strip() for k in subject_entry.get().split(',') if k.strip()]
            if body_entry.get().strip():
                conditions['body_keywords'] = [k.strip() for k in body_entry.get().split(',') if k.strip()]
            if from_entry.get().strip():
                conditions['from_contains'] = [f.strip() for f in from_entry.get().split(',') if f.strip()]
            if regex_entry.get().strip():
                conditions['subject_regex'] = regex_entry.get().strip()
            
            rule['conditions'] = conditions
            
            try:
                with open(self.rules_path, 'w', encoding='utf-8') as f:
                    yaml.dump(self.rules_data, f, allow_unicode=True, default_flow_style=False)
                messagebox.showinfo("Success", "Rule updated successfully!")
                dialog.destroy()
                self.refresh_rules()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save rule: {e}")
        
        tk.Button(
            dialog,
            text="💾 Save",
            font=('Arial', 11, 'bold'),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2',
            command=save_rule
        ).pack(pady=20)
        
    def toggle_rule(self):
        """Toggle rule enabled/disabled"""
        selection = self.rules_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a rule")
            return
        
        item = self.rules_tree.item(selection[0])
        rule_name = item['values'][0]
        
        for rule in self.rules_data.get('rules', []):
            if rule.get('name') == rule_name:
                rule['enabled'] = not rule.get('enabled', True)
                try:
                    with open(self.rules_path, 'w', encoding='utf-8') as f:
                        yaml.dump(self.rules_data, f, allow_unicode=True, default_flow_style=False)
                    messagebox.showinfo("Success", f"Rule {'enabled' if rule['enabled'] else 'disabled'}!")
                    self.refresh_rules()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update rule: {e}")
                break
                
    def delete_rule(self):
        """Delete selected rule"""
        selection = self.rules_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a rule")
            return
        
        item = self.rules_tree.item(selection[0])
        rule_name = item['values'][0]
        
        if messagebox.askyesno("Confirm", f"Delete rule '{rule_name}'?"):
            for i, rule in enumerate(self.rules_data.get('rules', [])):
                if rule.get('name') == rule_name:
                    self.rules_data['rules'].pop(i)
                    try:
                        with open(self.rules_path, 'w', encoding='utf-8') as f:
                            yaml.dump(self.rules_data, f, allow_unicode=True, default_flow_style=False)
                        messagebox.showinfo("Success", "Rule deleted!")
                        self.refresh_rules()
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to delete rule: {e}")
                    break
                    
    def refresh_logs(self):
        """Refresh logs display"""
        self.logs_text.delete('1.0', tk.END)
        
        # Read routing log
        try:
            if os.path.exists('routing_log.json'):
                with open('routing_log.json', 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        for line in lines[-50:]:  # Last 50 entries
                            try:
                                log = json.loads(line)
                                timestamp = log.get('timestamp', 'Unknown')
                                from_addr = log.get('from', 'Unknown')
                                subject = log.get('subject', 'No Subject')
                                rule = log.get('rule_name', 'Unknown')
                                forwarded_to = ', '.join(log.get('forwarded_to', []))
                                
                                self.logs_text.insert(tk.END, f"[{timestamp}]\n", 'timestamp')
                                self.logs_text.insert(tk.END, f"  From: {from_addr}\n", 'normal')
                                self.logs_text.insert(tk.END, f"  Subject: {subject}\n", 'normal')
                                self.logs_text.insert(tk.END, f"  Rule: {rule}\n", 'normal')
                                self.logs_text.insert(tk.END, f"  Forwarded To: {forwarded_to}\n\n", 'normal')
                            except:
                                pass
            else:
                self.logs_text.insert(tk.END, "No routing logs found yet.\n")
        except Exception as e:
            self.logs_text.insert(tk.END, f"Error reading logs: {e}\n")
        
        # Read application log
        try:
            if os.path.exists('email_router.log'):
                with open('email_router.log', 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        self.logs_text.insert(tk.END, "\n" + "="*80 + "\n")
                        self.logs_text.insert(tk.END, "APPLICATION LOG\n")
                        self.logs_text.insert(tk.END, "="*80 + "\n\n")
                        for line in lines[-100:]:  # Last 100 lines
                            self.logs_text.insert(tk.END, line)
        except:
            pass
        
        # Configure text tags for styling
        self.logs_text.tag_config('timestamp', foreground='#4EC9B0')
        self.logs_text.tag_config('normal', foreground='#D4D4D4')
        
        # Scroll to bottom
        self.logs_text.see(tk.END)
        
    def start_router(self):
        """Start the email router"""
        if self.is_running:
            return
        
        # Check if config exists
        if not os.path.exists(self.config_path):
            messagebox.showerror("Error", "Configuration file not found!\nPlease configure settings first.")
            return
        
        try:
            self.router = EmailRouter(config_path=self.config_path)
            self.is_running = True
            
            # Start router in background thread
            self.router_thread = threading.Thread(target=self.run_router_continuous, daemon=True)
            self.router_thread.start()
            
            # Update UI
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_indicator.config(fg=self.colors['success'])
            self.status_label.config(text="Running")
            
            messagebox.showinfo("Success", "Email router started!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start router:\n{e}")
            self.is_running = False
            
    def stop_router(self):
        """Stop the email router"""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Update UI
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_indicator.config(fg=self.colors['danger'])
        self.status_label.config(text="Stopped")
        
        messagebox.showinfo("Info", "Email router stopped.")
        
    def run_router_continuous(self):
        """Run router continuously"""
        interval = self.config.get('check_interval', 60)
        while self.is_running:
            try:
                self.router.run_once()
                # Update UI from main thread
                self.root.after(0, self.update_last_check_time)
                time.sleep(interval)
            except Exception as e:
                if self.is_running:
                    logger.error(f"Error in router: {e}")
                    time.sleep(interval)
                    
    def update_last_check_time(self):
        """Update last check time label (called from main thread)"""
        if hasattr(self, 'last_check_label'):
            self.last_check_label.config(text=f"Last Check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
    def run_once(self):
        """Run router once"""
        def run_in_thread():
            try:
                if not os.path.exists(self.config_path):
                    self.root.after(0, lambda: messagebox.showerror("Error", "Configuration file not found!"))
                    return
                
                router = EmailRouter(config_path=self.config_path)
                router.run_once()
                self.root.after(0, self.update_last_check_time)
                self.root.after(0, lambda: messagebox.showinfo("Success", "Email processing completed!"))
                self.root.after(0, self.refresh_logs)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Error processing emails:\n{e}"))
        
        # Run in background thread to avoid blocking UI
        threading.Thread(target=run_in_thread, daemon=True).start()
            
    def update_status(self):
        """Update status periodically"""
        self.update_failed_count()
        # This will be called periodically to update status
        self.root.after(5000, self.update_status)
    
    def update_failed_count(self):
        """Update failed emails count"""
        try:
            failed_file = 'failed_emails.txt'
            failed_count = 0
            if os.path.exists(failed_file):
                with open(failed_file, 'r', encoding='utf-8') as f:
                    failed_count = len([line for line in f if line.strip()])
            
            if hasattr(self, 'failed_emails_label'):
                if failed_count > 0:
                    self.failed_emails_label.config(
                        text=str(failed_count),
                        fg=self.colors['warning']
                    )
                else:
                    self.failed_emails_label.config(
                        text="0",
                        fg=self.colors['success']
                    )
        except Exception as e:
            logger.error(f"Error updating failed count: {e}")
    
    def retry_failed_emails(self):
        """Retry processing failed emails"""
        def run_retry():
            try:
                if not os.path.exists(self.config_path):
                    self.root.after(0, lambda: messagebox.showerror("Error", "Configuration file not found!"))
                    return
                
                router = EmailRouter(config_path=self.config_path)
                # Process inbox with retry for failed emails
                router.process_inbox(include_read=True)
                self.root.after(0, self.update_failed_count)
                self.root.after(0, lambda: messagebox.showinfo("Success", "Failed emails retry completed!"))
                self.root.after(0, self.refresh_logs)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Error retrying failed emails:\n{e}"))
        
        threading.Thread(target=run_retry, daemon=True).start()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ModernGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

