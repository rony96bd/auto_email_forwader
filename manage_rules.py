#!/usr/bin/env python3
"""
Email Routing Rules Manager
ইমেইল রাউটিং রুলস ম্যানেজার

A simple command-line tool to manage routing rules without editing YAML files directly.
"""

import yaml
import sys
from typing import List, Dict
import json


class RulesManager:
    """Manage email routing rules"""
    
    def __init__(self, rules_file: str = 'routing_rules.yaml'):
        self.rules_file = rules_file
        self.rules_data = self.load_rules()
    
    def load_rules(self) -> Dict:
        """Load routing rules from file"""
        try:
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {'rules': []}
    
    def save_rules(self):
        """Save routing rules to file"""
        with open(self.rules_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.rules_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"✓ Rules saved to {self.rules_file}")
    
    def list_rules(self):
        """List all routing rules"""
        rules = self.rules_data.get('rules', [])
        
        if not rules:
            print("No routing rules defined.")
            return
        
        print("\n" + "="*80)
        print("EMAIL ROUTING RULES / ইমেইল রাউটিং রুলস")
        print("="*80)
        
        for i, rule in enumerate(rules, 1):
            status = "✓ ENABLED" if rule.get('enabled', True) else "✗ DISABLED"
            print(f"\n[{i}] {rule.get('name', 'Unnamed Rule')} - {status}")
            print(f"    Match Type: {rule.get('match_type', 'any')}")
            
            conditions = rule.get('conditions', {})
            if 'subject_keywords' in conditions:
                print(f"    Subject Keywords: {', '.join(conditions['subject_keywords'])}")
            if 'body_keywords' in conditions:
                print(f"    Body Keywords: {', '.join(conditions['body_keywords'])}")
            if 'from_contains' in conditions:
                print(f"    From Contains: {', '.join(conditions['from_contains'])}")
            if 'subject_regex' in conditions:
                print(f"    Subject Regex: {conditions['subject_regex']}")
            
            forward_to = rule.get('forward_to', [])
            print(f"    Forward To: {', '.join(forward_to)}")
        
        # Show default rule
        default_rule = self.rules_data.get('default_rule')
        if default_rule:
            status = "✓ ENABLED" if default_rule.get('enabled', False) else "✗ DISABLED"
            print(f"\n[DEFAULT] {default_rule.get('name', 'Default Rule')} - {status}")
            print(f"    Forward To: {', '.join(default_rule.get('forward_to', []))}")
        
        print("\n" + "="*80)
    
    def add_rule(self):
        """Add a new routing rule interactively"""
        print("\n" + "="*80)
        print("ADD NEW ROUTING RULE / নতুন রাউটিং রুল যোগ করুন")
        print("="*80)
        
        rule = {}
        
        # Name
        rule['name'] = input("\nRule Name / রুলের নাম: ").strip()
        if not rule['name']:
            print("Error: Rule name is required!")
            return
        
        # Enabled
        enabled = input("Enable this rule? (Y/n) / রুল চালু করবেন? (Y/n): ").strip().lower()
        rule['enabled'] = enabled != 'n'
        
        # Match type
        print("\nMatch Type / ম্যাচ টাইপ:")
        print("  1. any  - যেকোনো একটি condition ম্যাচ করলেই হবে")
        print("  2. all  - সব condition ম্যাচ করতে হবে")
        match_choice = input("Choose (1/2) [default: 1]: ").strip()
        rule['match_type'] = 'all' if match_choice == '2' else 'any'
        
        # Conditions
        conditions = {}
        
        print("\n--- Conditions / শর্তসমূহ ---")
        
        # Subject keywords
        subject_kw = input("\nSubject Keywords (comma separated) / সাবজেক্ট কীওয়ার্ড (কমা দিয়ে আলাদা করুন): ").strip()
        if subject_kw:
            conditions['subject_keywords'] = [kw.strip() for kw in subject_kw.split(',')]
        
        # Body keywords
        body_kw = input("Body Keywords (comma separated) / বডি কীওয়ার্ড (কমা দিয়ে আলাদা করুন): ").strip()
        if body_kw:
            conditions['body_keywords'] = [kw.strip() for kw in body_kw.split(',')]
        
        # From contains
        from_contains = input("Sender Email Contains (comma separated) / প্রেরকের ইমেইলে থাকবে (কমা দিয়ে আলাদা করুন): ").strip()
        if from_contains:
            conditions['from_contains'] = [fc.strip() for fc in from_contains.split(',')]
        
        # Subject regex (advanced)
        use_regex = input("Use regex pattern? (y/N) / Regex ব্যবহার করবেন? (y/N): ").strip().lower()
        if use_regex == 'y':
            regex = input("Subject Regex Pattern: ").strip()
            if regex:
                conditions['subject_regex'] = regex
        
        if not conditions:
            print("Error: At least one condition is required!")
            return
        
        rule['conditions'] = conditions
        
        # Forward to
        print("\n--- Forward To / যেখানে পাঠাবে ---")
        forward_to = []
        while True:
            email = input(f"Insurance Company Email {len(forward_to)+1} (Enter to finish) / ইন্সুরেন্স কোম্পানি ইমেইল {len(forward_to)+1} (Enter চাপলে শেষ হবে): ").strip()
            if not email:
                break
            forward_to.append(email)
        
        if not forward_to:
            print("Error: At least one recipient email is required!")
            return
        
        rule['forward_to'] = forward_to
        
        # Confirm
        print("\n--- Rule Preview / রুল প্রিভিউ ---")
        print(json.dumps(rule, indent=2, ensure_ascii=False))
        
        confirm = input("\nSave this rule? (Y/n) / এই রুল সেভ করবেন? (Y/n): ").strip().lower()
        if confirm != 'n':
            if 'rules' not in self.rules_data:
                self.rules_data['rules'] = []
            self.rules_data['rules'].append(rule)
            self.save_rules()
            print("✓ Rule added successfully!")
        else:
            print("Rule not saved.")
    
    def enable_rule(self, rule_index: int):
        """Enable a rule"""
        rules = self.rules_data.get('rules', [])
        if 1 <= rule_index <= len(rules):
            rules[rule_index - 1]['enabled'] = True
            self.save_rules()
            print(f"✓ Rule {rule_index} enabled")
        else:
            print(f"Error: Rule {rule_index} not found")
    
    def disable_rule(self, rule_index: int):
        """Disable a rule"""
        rules = self.rules_data.get('rules', [])
        if 1 <= rule_index <= len(rules):
            rules[rule_index - 1]['enabled'] = False
            self.save_rules()
            print(f"✓ Rule {rule_index} disabled")
        else:
            print(f"Error: Rule {rule_index} not found")
    
    def delete_rule(self, rule_index: int):
        """Delete a rule"""
        rules = self.rules_data.get('rules', [])
        if 1 <= rule_index <= len(rules):
            rule_name = rules[rule_index - 1].get('name', 'Unnamed')
            confirm = input(f"Delete rule '{rule_name}'? (y/N): ").strip().lower()
            if confirm == 'y':
                rules.pop(rule_index - 1)
                self.save_rules()
                print(f"✓ Rule {rule_index} deleted")
            else:
                print("Deletion cancelled")
        else:
            print(f"Error: Rule {rule_index} not found")
    
    def edit_rule(self, rule_index: int):
        """Edit a rule"""
        rules = self.rules_data.get('rules', [])
        if not (1 <= rule_index <= len(rules)):
            print(f"Error: Rule {rule_index} not found")
            return
        
        rule = rules[rule_index - 1]
        print(f"\nEditing Rule: {rule.get('name', 'Unnamed')}")
        print("\nCurrent configuration:")
        print(json.dumps(rule, indent=2, ensure_ascii=False))
        
        print("\nWhat would you like to edit?")
        print("1. Name")
        print("2. Enable/Disable")
        print("3. Forward To addresses")
        print("4. Conditions")
        print("5. Cancel")
        
        choice = input("Choose (1-5): ").strip()
        
        if choice == '1':
            new_name = input(f"New name [{rule.get('name')}]: ").strip()
            if new_name:
                rule['name'] = new_name
                self.save_rules()
                print("✓ Name updated")
        
        elif choice == '2':
            rule['enabled'] = not rule.get('enabled', True)
            self.save_rules()
            status = "enabled" if rule['enabled'] else "disabled"
            print(f"✓ Rule {status}")
        
        elif choice == '3':
            print("\nCurrent addresses:", ', '.join(rule.get('forward_to', [])))
            print("Enter new addresses (comma separated, or press Enter to keep current):")
            new_addresses = input().strip()
            if new_addresses:
                rule['forward_to'] = [addr.strip() for addr in new_addresses.split(',')]
                self.save_rules()
                print("✓ Forward addresses updated")
        
        elif choice == '4':
            print("\nEditing conditions is complex. Please edit the YAML file directly.")
            print(f"File: {self.rules_file}")
        
        else:
            print("Edit cancelled")
    
    def show_logs(self, limit: int = 20):
        """Show recent routing logs"""
        try:
            with open('routing_log.json', 'r', encoding='utf-8') as f:
                logs = [json.loads(line) for line in f.readlines()]
            
            print("\n" + "="*80)
            print(f"RECENT ROUTING LOGS (Last {limit})")
            print("="*80)
            
            for log in logs[-limit:]:
                print(f"\n[{log.get('timestamp', 'Unknown')}]")
                print(f"  From: {log.get('from', 'Unknown')}")
                print(f"  Subject: {log.get('subject', 'No Subject')}")
                print(f"  Rule: {log.get('rule_name', 'Unknown')}")
                print(f"  Forwarded To: {', '.join(log.get('forwarded_to', []))}")
            
            print("\n" + "="*80)
            
        except FileNotFoundError:
            print("No routing logs found yet.")
        except Exception as e:
            print(f"Error reading logs: {e}")


def print_menu():
    """Print main menu"""
    print("\n" + "="*80)
    print("EMAIL ROUTING RULES MANAGER / ইমেইল রাউটিং রুলস ম্যানেজার")
    print("="*80)
    print("\n1. List all rules / সব রুল দেখুন")
    print("2. Add new rule / নতুন রুল যোগ করুন")
    print("3. Enable rule / রুল চালু করুন")
    print("4. Disable rule / রুল বন্ধ করুন")
    print("5. Edit rule / রুল এডিট করুন")
    print("6. Delete rule / রুল মুছুন")
    print("7. Show routing logs / রাউটিং লগ দেখুন")
    print("8. Exit / বের হন")
    print("\n" + "="*80)


def main():
    """Main entry point"""
    manager = RulesManager()
    
    while True:
        print_menu()
        choice = input("\nChoose an option / একটি অপশন বেছে নিন (1-8): ").strip()
        
        if choice == '1':
            manager.list_rules()
        
        elif choice == '2':
            manager.add_rule()
        
        elif choice == '3':
            manager.list_rules()
            rule_num = input("\nEnter rule number to enable / চালু করতে রুল নম্বর দিন: ").strip()
            try:
                manager.enable_rule(int(rule_num))
            except ValueError:
                print("Invalid rule number")
        
        elif choice == '4':
            manager.list_rules()
            rule_num = input("\nEnter rule number to disable / বন্ধ করতে রুল নম্বর দিন: ").strip()
            try:
                manager.disable_rule(int(rule_num))
            except ValueError:
                print("Invalid rule number")
        
        elif choice == '5':
            manager.list_rules()
            rule_num = input("\nEnter rule number to edit / এডিট করতে রুল নম্বর দিন: ").strip()
            try:
                manager.edit_rule(int(rule_num))
            except ValueError:
                print("Invalid rule number")
        
        elif choice == '6':
            manager.list_rules()
            rule_num = input("\nEnter rule number to delete / মুছে ফেলতে রুল নম্বর দিন: ").strip()
            try:
                manager.delete_rule(int(rule_num))
            except ValueError:
                print("Invalid rule number")
        
        elif choice == '7':
            limit = input("How many logs to show? (default: 20): ").strip()
            try:
                limit = int(limit) if limit else 20
            except ValueError:
                limit = 20
            manager.show_logs(limit)
        
        elif choice == '8':
            print("\nThank you for using Email Routing Rules Manager!")
            print("ইমেইল রাউটিং রুলস ম্যানেজার ব্যবহার করার জন্য ধন্যবাদ!")
            break
        
        else:
            print("Invalid choice. Please choose 1-8.")
        
        input("\nPress Enter to continue...")


if __name__ == '__main__':
    main()
