#!/bin/bash

echo "=== FLASK-BABEL TRANSLATION VERIFICATION ==="
echo ""

# 1. Count msgid entries
echo "1. Counting translation entries..."
POT_COUNT=$(grep -c "^msgid" messages.pot 2>/dev/null || echo "0")
RO_COUNT=$(grep -c "^msgid" translations/ro/LC_MESSAGES/messages.po 2>/dev/null || echo "0")
ES_COUNT=$(grep -c "^msgid" translations/es/LC_MESSAGES/messages.po 2>/dev/null || echo "0")

echo "   messages.pot: $POT_COUNT entries"
echo "   Romanian: $RO_COUNT entries"
echo "   Spanish: $ES_COUNT entries"

if [ "$POT_COUNT" -eq "$RO_COUNT" ] && [ "$POT_COUNT" -eq "$ES_COUNT" ]; then
    echo "   ✅ All files have matching entry counts"
else
    echo "   ❌ Entry count mismatch detected"
fi

echo ""

# 2. Find empty translations
echo "2. Checking for empty translations..."
RO_EMPTY=$(grep -B 1 '^msgstr ""$' translations/ro/LC_MESSAGES/messages.po 2>/dev/null | grep "^msgid" | grep -v 'msgid ""' | wc -l)
ES_EMPTY=$(grep -B 1 '^msgstr ""$' translations/es/LC_MESSAGES/messages.po 2>/dev/null | grep "^msgid" | grep -v 'msgid ""' | wc -l)

echo "   Romanian empty: $RO_EMPTY"
echo "   Spanish empty: $ES_EMPTY"

if [ "$RO_EMPTY" -eq 0 ] && [ "$ES_EMPTY" -eq 0 ]; then
    echo "   ✅ No empty translations"
else
    echo "   ❌ Empty translations found"
fi

echo ""

# 3. Find fuzzy translations
echo "3. Checking for fuzzy translations..."
RO_FUZZY=$(grep -c "#, fuzzy" translations/ro/LC_MESSAGES/messages.po 2>/dev/null || echo "0")
ES_FUZZY=$(grep -c "#, fuzzy" translations/es/LC_MESSAGES/messages.po 2>/dev/null || echo "0")

echo "   Romanian fuzzy: $RO_FUZZY"
echo "   Spanish fuzzy: $ES_FUZZY"

if [ "$RO_FUZZY" -eq 0 ] && [ "$ES_FUZZY" -eq 0 ]; then
    echo "   ✅ No fuzzy translations"
else
    echo "   ❌ Fuzzy translations found"
fi

echo ""

# 4. Check .mo files exist and are recent
echo "4. Verifying compiled .mo files..."
if [ -f "translations/ro/LC_MESSAGES/messages.mo" ] && [ -f "translations/es/LC_MESSAGES/messages.mo" ]; then
    echo "   ✅ Both .mo files exist"
    
    # Check if .mo is newer than .po
    if [ "translations/ro/LC_MESSAGES/messages.mo" -nt "translations/ro/LC_MESSAGES/messages.po" ] && \
       [ "translations/es/LC_MESSAGES/messages.mo" -nt "translations/es/LC_MESSAGES/messages.po" ]; then
        echo "   ✅ .mo files are up to date"
    else
        echo "   ⚠️  .mo files may be outdated - run: pybabel compile -d translations"
    fi
else
    echo "   ❌ .mo files missing - run: pybabel compile -d translations"
fi

echo ""

# 5. Check for hardcoded strings in templates
echo "5. Scanning templates for hardcoded English..."
HARDCODED=$(find templates/ -name "*.html" -exec grep -l '<h[1-6][^>]*>[^{<]*[A-Za-z]' {} \; 2>/dev/null | grep -v "{{ _(" | wc -l)
echo "   Potential hardcoded headings found in: $HARDCODED files"

if [ "$HARDCODED" -eq 0 ]; then
    echo "   ✅ No obvious hardcoded strings detected"
else
    echo "   ⚠️  Manual review recommended"
fi

echo ""

# 6. Template-by-template analysis
echo "6. Template-by-template hardcoded string check..."
for template in templates/*.html; do
    if [ -f "$template" ]; then
        basename_template=$(basename "$template")
        hardcoded_count=$(grep -c '<[^>]*>[^{<]*[A-Za-z][^<]*</' "$template" 2>/dev/null | grep -v "{{ _(" | head -1)
        if [ "$hardcoded_count" -gt 0 ]; then
            echo "   ⚠️  $basename_template: $hardcoded_count potential hardcoded strings"
        else
            echo "   ✅ $basename_template: No hardcoded strings detected"
        fi
    fi
done

echo ""
echo "=== VERIFICATION COMPLETE ==="
