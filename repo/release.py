#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET
import hashlib

def main():
    if len(sys.argv) != 5:
        print("Usage: release.py <repofile> <version> <zipfile> <url>")
        sys.exit(1)

    repofile = sys.argv[1]
    version = sys.argv[2]
    zipfile = sys.argv[3]
    url = sys.argv[4]

    # Calculate SHA-1 hash of zipfile
    sha = hashlib.sha1()
    with open(zipfile, 'rb') as f:
        sha.update(f.read())
    sha_hex = sha.hexdigest()

    # Parse XML
    tree = ET.parse(repofile)
    root = tree.getroot()

    # Navigate to the plugin element
    # Structure: extensions > plugins > plugin
    plugin = root.find('.//plugin')

    if plugin is None:
        print("Error: Could not find plugin element in XML", file=sys.stderr)
        sys.exit(1)

    # Update version attribute
    plugin.set('version', version)

    # Update SHA
    sha_elem = plugin.find('sha')
    if sha_elem is not None:
        sha_elem.text = sha_hex
    else:
        sha_elem = ET.SubElement(plugin, 'sha')
        sha_elem.text = sha_hex

    # Update URL
    url_elem = plugin.find('url')
    full_url = f"{url}/{zipfile}"
    if url_elem is not None:
        url_elem.text = full_url
    else:
        url_elem = ET.SubElement(plugin, 'url')
        url_elem.text = full_url

    # Write XML back
    tree.write(repofile, encoding='UTF-8', xml_declaration=True)

    # Print result
    print(f"version:{version} sha:{sha_hex}")

if __name__ == '__main__':
    main()
