"""MailChimp related commands for dhutil's CLI."""

import click

from dhutil.mailchimp_utils import (
    list_lists,
    sync_mailchimp_registrants,
    sync_mailchimp_accepted,
)


@click.group(help="MailChimp related commands.")
def mailchimp():
    """MailChimp related commands."""
    pass


@mailchimp.command(help="List all MailChimp lists.")
def lists():
    """List all MailChimp lists."""
    list_lists()


@mailchimp.command(help="Sync MailChimp registrants list.")
def sync_reg():
    """Sync MailChimp registrants list."""
    sync_mailchimp_registrants()


@mailchimp.command(help="Sync MailChimp accepted list.")
def sync_accepted():
    """Sync MailChimp accepted list."""
    sync_mailchimp_accepted()
