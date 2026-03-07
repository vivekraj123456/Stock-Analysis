#!/bin/bash
# ═══════════════════════════════════════════════════════════
#  AUTO STOCK UPDATER — Mac / Linux cron setup
# ═══════════════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$SCRIPT_DIR/fetch_clean_stocks.py"
LOG="$SCRIPT_DIR/powerbi_data/scheduler.log"
PYTHON=$(which python3)

echo "Script : $SCRIPT"
echo "Python : $PYTHON"
echo "Log    : $LOG"
echo ""

# Add cron job: runs every weekday at 7:00 AM
CRON_JOB="0 7 * * 1-5 $PYTHON $SCRIPT >> $LOG 2>&1"
(crontab -l 2>/dev/null | grep -v "fetch_clean_stocks"; echo "$CRON_JOB") | crontab -

echo "✅  Cron job installed!"
echo "    Schedule: Every weekday at 7:00 AM"
echo ""
echo "To verify:  crontab -l"
echo "To remove:  crontab -e  (delete the line manually)"
