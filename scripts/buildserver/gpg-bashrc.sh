# Add this to your ~/.bashrc or ~/.bash_profile
# This will automatically preset your GPG passphrase when you log in

# Your GPG signing key's keygrip
export GPG_KEYGRIP="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Replace with your actual keygrip

# Function to check if GPG passphrase is already preset
gpg_session_is_ready() {
    # Try a test signing operation
        gpg-connect-agent "keyinfo ${GPG_KEYGRIP}" /bye 2>/dev/null | grep -q "1 P"
}

# Auto-initialize GPG session on login (only if not already initialized)
if [ -n "$GPG_KEYGRIP" ] && [ "$GPG_KEYGRIP" != "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" ]; then
    if ! gpg_session_is_ready; then
        echo "Initializing GPG session..."
        source ~/bin/global.sh
        preset_gpg_passphrase "$GPG_KEYGRIP"

        if [ $? -eq 0 ]; then
            echo "✓ GPG session ready for package signing"
        fi
    fi
fi
