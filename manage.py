import argparse
import logging

from config import load_config, save_config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def add_query(args):
    config = load_config()
    for q in config['queries']:
        if q['name'] == args.name:
            logger.error('Query %s already exists', args.name)
            return
    config['queries'].append({'name': args.name, 'sql': args.sql, 'recipients': args.recipients})
    save_config(config)


def remove_query(args):
    config = load_config()
    config['queries'] = [q for q in config['queries'] if q['name'] != args.name]
    save_config(config)


def list_queries(_args):
    config = load_config()
    for q in config['queries']:
        print(q['name'])


def add_recipient(args):
    config = load_config()
    for q in config['queries']:
        if q['name'] == args.name:
            if args.email not in q['recipients']:
                q['recipients'].append(args.email)
            break
    save_config(config)


def remove_recipient(args):
    config = load_config()
    for q in config['queries']:
        if q['name'] == args.name:
            q['recipients'] = [e for e in q['recipients'] if e != args.email]
            break
    save_config(config)


def set_schedule(args):
    config = load_config()
    config['schedule_cron'] = args.cron
    save_config(config)


def show_config(_args):
    print(load_config())


def main():
    parser = argparse.ArgumentParser(description='Manage report configuration')
    sub = parser.add_subparsers(dest='cmd')

    aq = sub.add_parser('add-query')
    aq.add_argument('--name', required=True)
    aq.add_argument('--sql', required=True)
    aq.add_argument('--recipients', nargs='*', default=[])
    aq.set_defaults(func=add_query)

    rq = sub.add_parser('remove-query')
    rq.add_argument('name')
    rq.set_defaults(func=remove_query)

    lq = sub.add_parser('list-queries')
    lq.set_defaults(func=list_queries)

    ar = sub.add_parser('add-recipient')
    ar.add_argument('name')
    ar.add_argument('email')
    ar.set_defaults(func=add_recipient)

    rr = sub.add_parser('remove-recipient')
    rr.add_argument('name')
    rr.add_argument('email')
    rr.set_defaults(func=remove_recipient)

    ss = sub.add_parser('set-schedule')
    ss.add_argument('cron')
    ss.set_defaults(func=set_schedule)

    sc = sub.add_parser('show-config')
    sc.set_defaults(func=show_config)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
