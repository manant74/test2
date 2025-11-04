#!/usr/bin/env python3
"""
Pre-Deployment Verification Script for VibeTheForce
Run this script before deploying to Streamlit Cloud to verify all files are ready.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ MISSING {description}: {filepath}")
        return False

def check_file_content(filepath, required_content, description):
    """Check if file contains required content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if required_content in content:
                print(f"✅ {description}")
                return True
            else:
                print(f"❌ {description} - Content not found")
                return False
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 VibeTheForce - Pre-Deployment Verification")
    print("=" * 60)
    print()
    
    all_checks_passed = True
    
    # Check core files
    print("📁 Checking Core Files...")
    all_checks_passed &= check_file_exists("app.py", "Main app file")
    all_checks_passed &= check_file_exists("requirements.txt", "Dependencies file")
    all_checks_passed &= check_file_exists(".python-version", "Python version file")
    all_checks_passed &= check_file_exists("README.md", "README file")
    print()
    
    # Check Streamlit configuration
    print("⚙️ Checking Streamlit Configuration...")
    all_checks_passed &= check_file_exists(".streamlit/config.toml", "Streamlit config")
    all_checks_passed &= check_file_exists(".streamlit/secrets.toml.example", "Secrets example")
    all_checks_passed &= check_file_content(
        ".streamlit/config.toml",
        "primaryColor",
        "Theme configuration present"
    )
    print()
    
    # Check database files
    print("🗄️ Checking Database Files...")
    all_checks_passed &= check_file_exists("database/db_manager.py", "Database manager")
    all_checks_passed &= check_file_exists("database/schema.sql", "Database schema")
    print()
    
    # Check services
    print("🔧 Checking Services...")
    all_checks_passed &= check_file_exists("services/vote_service.py", "Vote service")
    all_checks_passed &= check_file_exists("services/analytics_service.py", "Analytics service")
    all_checks_passed &= check_file_exists("services/gemini_client.py", "Gemini client")
    print()
    
    # Check pages
    print("📄 Checking Streamlit Pages...")
    all_checks_passed &= check_file_exists("pages/1_🗳️_Vota.py", "Voting page")
    all_checks_passed &= check_file_exists("pages/2_📊_Risultati.py", "Results page")
    all_checks_passed &= check_file_exists("pages/3_⚙️_Admin.py", "Admin page")
    print()
    
    # Check utilities
    print("🛠️ Checking Utilities...")
    all_checks_passed &= check_file_exists("utils/theme.py", "Theme utility")
    all_checks_passed &= check_file_exists("utils/qr_generator.py", "QR generator")
    print()
    
    # Check requirements.txt content
    print("📦 Checking Dependencies...")
    required_packages = [
        "streamlit",
        "google-generativeai",
        "plotly",
        "pandas",
        "qrcode"
    ]
    
    try:
        with open("requirements.txt", 'r') as f:
            requirements_content = f.read()
            for package in required_packages:
                if package in requirements_content:
                    print(f"✅ {package} in requirements.txt")
                else:
                    print(f"❌ {package} MISSING from requirements.txt")
                    all_checks_passed = False
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        all_checks_passed = False
    print()
    
    # Check .gitignore
    print("🚫 Checking .gitignore...")
    all_checks_passed &= check_file_content(
        ".gitignore",
        ".streamlit/secrets.toml",
        "Secrets excluded from git"
    )
    all_checks_passed &= check_file_content(
        ".gitignore",
        "votes.db",
        "Database excluded from git"
    )
    print()
    
    # Check deployment documentation
    print("📚 Checking Documentation...")
    all_checks_passed &= check_file_exists("DEPLOYMENT.md", "Deployment guide")
    all_checks_passed &= check_file_exists("DEPLOY_INSTRUCTIONS.md", "Deploy instructions")
    print()
    
    # Final summary
    print("=" * 60)
    if all_checks_passed:
        print("✅ ALL CHECKS PASSED! Ready for deployment! 🚀")
        print()
        print("Next steps:")
        print("1. Push to GitHub: git push origin main")
        print("2. Deploy on Streamlit Cloud: https://share.streamlit.io")
        print("3. Configure GEMINI_API_KEY in Secrets")
        print("4. Verify app loads in < 3 seconds")
        print()
        print("See DEPLOY_INSTRUCTIONS.md for detailed steps.")
        return 0
    else:
        print("❌ SOME CHECKS FAILED! Please fix the issues above.")
        print()
        print("Review the missing files or configurations and try again.")
        return 1
    print("=" * 60)

if __name__ == "__main__":
    sys.exit(main())
