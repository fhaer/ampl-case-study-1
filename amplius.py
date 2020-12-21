import sys
import uuid
import getopt

from ampl import attestation
from ampl import transfer
from ampl import identity

def print_usage():
    print("Usage: amplius.py <command> [argument]*")
    print("")
    print("Amplius a user interface for creating and verifying attested multi-protocol links (AMPL). The prototype supports the transfer clients IPFS, Git, and HTTP.")
    print("")
    print("<command> is one of the following attestation, identity, or transfer commands.")
    print("")
    print("Attestation Commands:")
    print("--attest [file]*                     create an identity, distribute all files, issue a content-based claim")
    print("--retrieve=<claim-id>                fetch and validate all files of the claim <claim-id>")
    print("--issue-claim [file]*                issue a content-based claim for all files")
    print("--issue-claim=UUID [file]*           issue a content-independent claim for all files with a random UUID v4 as claim ID")
    print("--issue-claim=<claim-id> [file]*     issue a claim for all files using the given <claim-id> (32-64 characters)")
    print("--validate-claim=<claim-id> [file]*  validate all files of the claim <claim-id>")
    print("")
    print("Identity Commands:")
    print("--eth-account-new                    create an identity for attestations")
    print("--eth-account-show                   show the current identity for attestations")
    print("")
    print("Transfer Commands:")
    print("--distribute [file]*                 distribute all files using all transfer clients with example repositores")
    print("--ipfs [file]*                       all files are added to IPFS and pinned at a remote node")
    print("--git=<URL> [file]*                  all files are added, committed and pushed to <URL>")
    print("--http=<URL> [file]*                 all files are sent within a POST request to <URL>")
    print("--fetch=<URI>                        fetch all files from an ipfs, git, or HTTP <URI>")
    sys.exit()

def attest(files):
    identity_eth_account_new()
    distribute(files)
    issue_claim("", files)

def retrieve(claim_id):
    attestation.retrieve(claim_id)

def issue_claim(arg_id, files):
    merkle_root = attestation.calculate_merkle_root(files)
    claim_id = ""
    if arg_id == "UUID":
        claim_id = uuid.uuid4()
    elif len(arg_id) >= 32 and len(arg_id) <= 64:
        claim_id = arg_id
    else:
        claim_id = merkle_root
    attestation.issue_claim(claim_id, merkle_root, len(files))

def validate_claim(claim_id, files):
    merkle_root_prime = attestation.calculate_merkle_root(files)
    attestation.validate_claim(claim_id, merkle_root_prime)

def identity_eth_account_show():
    account_address = identity.get_identity()
    print(account_address)

def identity_eth_account_new():
    account_address = identity.initialize_identity()
    print(account_address)

def distribute(files):
    transfer.distribute(files)

def distribute_ipfs(files):
    transfer.distribute_ipfs(files)

def distribute_git(url, files):
    transfer.distribute_git(url, files)

def distribute_http(url, files):
    transfer.distribute_http(url, files)

def fetch(uri):
    transfer.fetch(uri)



def parse_cli():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "arivedighf", 
            ["attest", "retrieve=", "issue-claim=", "validate-claim=",
            "eth-account-new", "eth-account-show", "distribute", "ipfs", "git=", "http=", "fetch="])
    except getopt.GetoptError as err:
        print(err)
        print_usage()

    if len(opts) < 1:
        print_usage()

    for o, a in opts:
        if o in ("-a", "--attest"):
            attest(args)
        elif o in ("-r", "--retrieve"):
            claim_id = a
            retrieve(claim_id)
        elif o in ("-i", "--issue-claim"):
            mode = a
            issue_claim(mode, args)
        elif o in ("-v", "--validate-claim"):
            claim_id = a
            validate_claim(claim_id, args)
        elif o in ("-e", "--eth-account-show"):
            identity_eth_account_show()
        elif o in ("-e", "--eth-account-new"):
            identity_eth_account_new()
        elif o in ("-d", "--distribute"):
            distribute(args)
        elif o in ("-i", "--ipfs"):
            distribute_ipfs(args)
        elif o in ("-g", "--git"):
            url = a
            distribute_git(url, args)
        elif o in ("-h", "--http"):
            url = a
            distribute_http(url, args)
        elif o in ("-f", "--fetch"):
            uri = a
            fetch(uri)
        else:
            print_usage()

parse_cli()
