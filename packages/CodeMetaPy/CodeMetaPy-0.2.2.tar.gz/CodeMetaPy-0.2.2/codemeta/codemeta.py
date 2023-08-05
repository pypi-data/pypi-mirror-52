#!/usr/bin/env python3

#This script converts software metadata
#from PyPI/distutils into a generic codemata form (https://codemeta.github.io/)
#can be extended for other input types too

# Maarten van Gompel
# CLST, Radboud University Nijmegen
# GPL v3

import sys
import argparse
import json
import os.path
import csv
import importlib
from collections import OrderedDict, defaultdict
try:
    import yaml
except ImportError:
    yaml = None
from nameparser import HumanName

class CWKey:
    """Crosswalk Keys, correspond with header label in crosswalk.csv"""
    PROP = "Property"
    PARENT = "Parent Type"
    TYPE = "Type"
    DESCRIPTION = "Description"
    PYPI = "Python Distutils (PyPI)"
    DEBIAN = "Debian Package"
    R = "R Package Description"
    NODEJS = "NodeJS"
    MAVEN = "Java (Maven)"
    DOAP = "DOAP"

PROVIDER_PYPI = {
    "@id": "https://pypi.org",
    "@type": "Organization",
    "name": "The Python Package Index",
    "url": "https://pypi.org",
}
PROVIDER_DEBIAN = {
    "@id": "https://www.debian.org",
    "@type": "Organization",
    "name": "The Debian Project",
    "url": "https://www.debian.org",
}
PROGLANG_PYTHON = {
    "@type": "ComputerLanguage",
    "name": "Python",
    "version": str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(sys.version_info.micro),
    "url": "https://www.python.org",
}

CONTEXT =  [
    "https://doi.org/10.5063/schema/codemeta-2.0",
    "http://schema.org",
]

ENTRYPOINT_CONTEXT = { #these are all custom extensions not in codemeta (yet)
    "entryPoints": { "@reverse": "schema:actionApplication" },
    "interfaceType": { "@id": "codemeta:interfaceType" }, #Type of the entrypoint's interface (e.g CLI, GUI, WUI, TUI, REST, SOAP, XMLRPC, LIB)
    "specification": { "@id": "codemeta:specification" , "@type":"@id"}, #A technical specification of the interface
    "mediatorApplication": {"@id": "codemeta:mediatorApplication", "@type":"@id" } #auxiliary software that provided/enabled this entrypoint
}


if yaml is not None:
    def represent_ordereddict(dumper, data):
        value = []

        for item_key, item_value in data.items():
            node_key = dumper.represent_data(item_key)
            node_value = dumper.represent_data(item_value)

            value.append((node_key, node_value))

        return yaml.nodes.MappingNode('tag:yaml.org,2002:map', value)

    yaml.add_representer(OrderedDict, represent_ordereddict)


def readcrosswalk(sourcekeys=(CWKey.PYPI,CWKey.DEBIAN)):
    mapping = defaultdict(dict)
    #pip may output things differently than recorded in distutils/setup.py, so we register some aliases:
    mapping[CWKey.PYPI]["home-page"] = "url"
    mapping[CWKey.PYPI]["summary"] = "description"
    props = {}
    crosswalkfile = os.path.join(os.path.dirname(__file__), 'schema','crosswalk.csv')
    with open(crosswalkfile, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            props[row[CWKey.PROP]] = {"PARENT": row[CWKey.PARENT], "TYPE": row[CWKey.TYPE], "DESCRIPTION": row[CWKey.DESCRIPTION] }
            for sourcekey in sourcekeys:
                if row[sourcekey]:
                    mapping[sourcekey][row[sourcekey].lower()] = row[CWKey.PROP]

    return props, mapping


def parsepip(data, lines, mapping=None, with_entrypoints=False, orcid_placeholder=False):
    """Parses pip show -v output and converts to codemeta"""
    if mapping is None:
        _, mapping = readcrosswalk((CWKey.PYPI,))
    section = None
    data["provider"] = PROVIDER_PYPI
    data["runtimePlatform"] =  "Python " + str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(sys.version_info.micro)
    if with_entrypoints:
        #not in official specification!!!
        data['entryPoints'] = []
    for line in lines:
        if line.strip() == "Classifiers:":
            section = "classifiers"
        elif line.strip() == "Entry-points:":
            section = "interfaces"
        elif section == "classifiers":
            fields = [ x.strip() for x in line.strip().split('::') ]
            pipkey = "classifiers['" + fields[0] + "']"
            pipkey = pipkey.lower()
            if pipkey in mapping[CWKey.PYPI]:
                data[mapping[CWKey.PYPI][pipkey]] = " :: ".join(fields[1:])
            elif fields[0].lower() in mapping[CWKey.PYPI]:
                data[mapping[CWKey.PYPI][fields[0].lower()]] = " :: ".join(fields[1:])
            elif fields[0] == "Intended Audience":
                data["audience"].append({
                    "@type": "Audience",
                    "audienceType": " :: ".join(fields[1:])
                })
            else:
                print("NOTICE: Classifier "  + fields[0] + " has no translation",file=sys.stderr)
        elif section == "interfaces" and with_entrypoints:
            if line.strip() == "[console_scripts]":
                pass
            elif line.find('=') != -1:
                fields = [ x.strip() for x in line.split('=') ]
                if len(fields) > 1:
                    module_name = fields[1].strip().split(':')[0]
                    try:
                        module = importlib.import_module(module_name)
                        description = module.__doc__
                    except:
                        description = ""
                else:
                    description = ""
                entrypoint = {
                    "@type": "EntryPoint", #we are interpreting this a bit liberally because it's usually used with HTTP webservices
                    "name": fields[0],
                    "urlTemplate": "file:///" + fields[0], #three slashes because we omit host, the 'file' is an executable/binary (rather liberal use)
                    "interfaceType": "CLI", #custom property, this needs to be moved to a more formal vocabulary  at some point
                }
                if description:
                    entrypoint['description'] = description
                data['entryPoints'].append(entrypoint) #the entryPoints relation is not in the specification, but our own invention, it is the reverse of the EntryPoint.actionApplication property
        else:
            try:
                key, value = (x.strip() for x in line.split(':',1))
            except:
                continue
            if key == "Author":
                humanname = HumanName(value.strip())
                data["author"].append({"@type":"Person", "givenName": humanname.first, "familyName": " ".join((humanname.middle, humanname.last)).strip() })
                if orcid_placeholder:
                    data["author"][-1]["@id"] = "https://orcid.org/EDIT_ME!"
            elif key == "Author-email":
                if data["author"]:
                    data["author"][-1]["email"] = value
            elif key == "Requires":
                for dependency in value.split(','):
                    dependency = dependency.strip()
                    if dependency:
                        data['softwareRequirements'].append({
                            "@type": "SoftwareApplication",
                            "identifier": dependency,
                            "name": dependency,
                            "provider": PROVIDER_PYPI,
                            "runtimePlatform": "Python " + str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(sys.version_info.micro)
                        })
            elif key == "Requires-External":
                for dependency in value.split(','):
                    dependency = dependency.strip()
                    if dependency:
                        data['softwareRequirements'].append({
                            "@type": "SoftwareApplication",
                            "identifier": dependency,
                            "name": dependency,
                        })
            elif key.lower() in mapping[CWKey.PYPI]:
                data[mapping[CWKey.PYPI][key.lower()]] = value
                if key == "Name":
                    data["identifier"] = value
            else:
                print("WARNING: No translation for pip key " + key,file=sys.stderr)
    if with_entrypoints:
        if not data['entryPoints'] or ('applicationCategory' in data and 'libraries' in data['applicationCategory'].lower()):
            #no entry points defined, assume this is a library
            data['interfaceType'] = "LIB"
    return data

def parseapt(data, lines, mapping=None, with_entrypoints=False, orcid_placeholder=False):
    """Parses apt show output and converts to codemeta"""
    if mapping is None:
        _, mapping = readcrosswalk((CWKey.DEBIAN,))
    provider = PROVIDER_DEBIAN
    description = ""
    parsedescription = False
    if with_entrypoints:
        #not in official specification!!!
        data['entryPoints'] = []
    for line in lines:
        if parsedescription and line and line[0] == ' ':
            description += line[1:] + " "
        else:
            try:
                key, value = (x.strip() for x in line.split(':',1))
            except:
                continue
            if key == "Origin":
                data["provider"] = value
            elif key == "Depends":
                for dependency in value.split(","):
                    dependency = dependency.strip().split(" ")[0].strip()
                    if dependency:
                        data['softwareRequirements'].append({
                            "@type": "SoftwareApplication",
                            "identifier": dependency,
                            "name": dependency,
                        })
            elif key == "Section":
                if "libs" in value or "libraries" in value:
                    if with_entrypoints: data['interfaceType'] = "LIB"
                    data['audience'] = "Developers"
                elif "utils" in value or "text" in value:
                    if with_entrypoints: data['interfaceType'] = "CLI"
                elif "devel" in value:
                    data['audience'] = "Developers"
                elif "science" in value:
                    data['audience'] = "Researchers"
            elif key == "Description":
                parsedescription = True
                description = value + "\n\n"
            elif key == "Homepage":
                data["url"] = value
            elif key == "Version":
                data["version"] = value
            elif key.lower() in mapping[CWKey.DEBIAN]:
                data[mapping[CWKey.DEBIAN][key.lower()]] = value
                if key == "Package":
                    data["identifier"] = value
                    data["name"] = value
            else:
                print("WARNING: No translation for APT key " + key,file=sys.stderr)
    if description:
        data["description"] = description
    return data


def clean(data):
    """Purge empty values, lowercase identifier"""
    purgekeys = []
    for k,v in data.items():
        if v is "" or v is None or (isinstance(v,(tuple, list)) and len(v) == 0):
            purgekeys.append(k)
        elif isinstance(v, (dict, OrderedDict)):
            clean(v)
        elif isinstance(v, (tuple, list)):
            data[k] = [ clean(x) if isinstance(x, (dict,OrderedDict)) else x for x in v ]
    for k in purgekeys:
        del data[k]
    if 'identifier' in data:
        data['identifier'] = data['identifier'].lower()
    return data

def resolve(data, idmap=None):
    """Resolve nodes that refer to an ID mentioned earlier"""
    if idmap is None: idmap = {}
    for k,v in data.items():
        if isinstance(v, (dict, OrderedDict)):
            if '@id' in v:
                if len(v) > 1:
                    #this is not a reference, register in idmap (possibly overwriting earlier definition!)
                    idmap[v['@id']] = v
                elif len(v) == 1:
                    #this is a reference
                    if v['@id'] in idmap:
                        data[k] = idmap[v['@id']]
                    else:
                        print("NOTICE: Unable to resolve @id " + v['@id'] ,file=sys.stderr)
            resolve(v, idmap)
        elif isinstance(v, (tuple, list)):
            data[k] = [ resolve(x,idmap) if isinstance(x, (dict,OrderedDict)) else x for x in v ]
    return data

def getregistry(identifier, registry):
    for tool in registry['@graph']:
        if tool['identifier'].lower() == identifier.lower():
            return tool
    raise KeyError(identifier)

def update(data, newdata):
    """recursive update, adds values whenever possible instead of replacing"""
    if isinstance(data, dict):
        for key, value in newdata.items():
            if key in data:
                if isinstance(value, dict):
                    update(data[key], value)
                elif isinstance(value, list):
                    for x in value:
                        if isinstance(data[key], dict ):
                            data[key] = [ data[key], x ]
                        elif x not in data[key]:
                            if isinstance(data[key], list):
                               data[key].append(x)
                else:
                    data[key] = value
            else:
                data[key] = value

def main():
    props, mapping = readcrosswalk()
    parser = argparse.ArgumentParser(description="Converter for Python Distutils (PyPI) Metadata to CodeMeta (JSON-LD) converter. Also supports conversion from other metadata types such as those from Debian packages. The tool can combine metadata from multiple sources.")
    parser.add_argument('-e','--with-entrypoints', dest="with_entrypoints", help="Add entry points (this is not in the official codemeta specification)", action='store_true',required=False)
    parser.add_argument('--with-orcid', dest="with_orcid", help="Add placeholders for ORCID, requires manual editing of the output to insert the actual ORCIDs", action='store_true',required=False)
    parser.add_argument('-o', dest='output',type=str,help="Metadata output type: json (default), yaml", action='store',required=False, default="json")
    parser.add_argument('-i', dest='input',type=str,help="Metadata input type: pip (python distutils packages, default), apt (debian packages), registry, json, yaml. May be a comma seperated list of multiple types if files are passed on the command line", action='store',required=False, default="pip")
    parser.add_argument('-r', dest='registry',type=str,help="The given registry file groups multiple JSON-LD metadata together in one JSON file. If specified, the file will be read (or created), and updated. This is a custom extension not part of the CodeMeta specification", action='store',required=False)
    parser.add_argument('inputfiles', nargs='*', help='Input files, set -i accordingly with the types (must contain as many items as passed!')
    for key, prop in sorted(props.items()):
        if key:
            parser.add_argument('--' + key,dest=key, type=str, help=prop['DESCRIPTION'] + " (Type: "  + prop['TYPE'] + ", Parent: " + prop['PARENT'] + ") [you can format the value string in json if needed]", action='store',required=False)
    args = parser.parse_args()

    if args.with_entrypoints:
        extracontext = [ENTRYPOINT_CONTEXT]
    else:
        extracontext = []

    if args.registry:
        if os.path.exists(args.registry):
            with open(args.registry, 'r', encoding='utf-8') as f:
                registry = json.load(f)
        else:
            print("Registry " + args.registry + " does not exist yet, creating anew...",file=sys.stderr)
            registry = {"@context": CONTEXT + extracontext, "@graph": []}
    else:
        registry = None
    if registry is not None and ('@context' not in registry or '@graph' not in registry):
        print("Registry " + args.registry + " has invalid (outdated?) format, ignoring and creating a new one...",file=sys.stderr)
        registry = {"@context": CONTEXT + extracontext, "@graph": []}

    inputfiles = []
    if args.inputfiles:
        if ',' in args.input:
            if len(args.input.split(",")) != len(args.inputfiles):
                print("Passed " + str(len(args.inputfiles)) + " files but specified only " + str(len(args.input)) + " input types!",file=sys.stderr)
            else:
                inputfiles = [ (open(f,'r',encoding='utf-8'), t) if f != '-' and t != 'registry' else ( (f,t) if t == 'registry' else (sys.stdin,t) ) for f,t in zip(args.inputfiles, args.input.split(',')) ]
        else:
            inputfiles = [ (open(f,'r',encoding='utf-8'), args.input) if f != '-' else (sys.stdin,args.input) for f in args.inputfiles ] #same type for all
    else:
        inputfiles = [(sys.stdin,args.input)]

    data = OrderedDict({ #values are overriden/extended later
        '@context': CONTEXT + extracontext,
        "@type": "SoftwareSourceCode",
        "identifier":"unknown",
        "name":"unknown",
        "version":"unknown",
        "description":"",
        "license":"unknown",
        "author": [],
        "softwareRequirements": [],
        "audience": []
    })
    for stream, inputtype in inputfiles:
        if inputtype == "registry":
            try:
                update(data, getregistry(stream, registry))
            except KeyError as e:
                print("ERROR: No such identifier in registry: ", stream,file=sys.stderr)
                sys.exit(3)
        elif inputtype in ("pip","python","distutils"):
            piplines = stream.read().split("\n")
            update(data, parsepip(data, piplines, mapping, args.with_entrypoints, args.with_orcid))
        elif inputtype in ("apt","debian","deb"):
            aptlines = stream.read().split("\n")
            update(data, parseapt(data, aptlines, mapping, args.with_entrypoints))
        elif inputtype == "json":
            update(data, json.load(stream))

        for key, prop in props.items():
            if hasattr(args,key) and getattr(args,key) is not None:
                value = getattr(args, key)
                try:
                    value = json.loads(value)
                except json.decoder.JSONDecodeError: #not JSON, take to be a literal string
                    if '[' in value or '{' in value: #surely this was meant to be json
                        raise
                data[key] = value

    data = clean(data)

    if args.output == "json":
        print(json.dumps(data, ensure_ascii=False, indent=4))
    elif args.output == "yaml":
        if not yaml:
            raise Exception("Yaml support not available", args.output)
        yaml.dump(data, sys.stdout, default_flow_style=False)
    else:
        raise Exception("No such output type: ", args.output)

    if args.registry:
        if '@context' in data:
            del data['@context'] #already in registry at top level
        data["@id"] = "#" + data['identifier'].lower()
        found = False
        for i, d in enumerate(registry["@graph"]):
            if d['identifier'].lower() == data['identifier'].lower():
                registry['@graph'][i] = data #overwrite existing entry
                found = True
                break
        if not found:
            registry["@graph"].append(data) #add new entry
        with open(args.registry,'w',encoding='utf-8') as f:
            print(json.dumps(registry, ensure_ascii=False, indent=4), file=f)

if __name__ == '__main__':
    main()
