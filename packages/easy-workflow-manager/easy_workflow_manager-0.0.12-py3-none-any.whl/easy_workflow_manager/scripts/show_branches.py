import click
import input_helper as ih
import easy_workflow_manager as ewm


@click.command()
@click.option(
    '--all', '-a', 'all_branches', is_flag=True, default=False,
    help='Show all remote branches (including QA)'
)
@click.option(
    '--local', '-l', 'local', is_flag=True, default=False,
    help='Also show local branches'
)
@click.argument('grep', nargs=1, default='')
def main(grep, all_branches, local):
    """Show branches that match specified grep pattern"""
    if local:
        print('\nRemote:')
    ewm.show_remote_branches(grep=grep, all_branches=all_branches)
    if local:
        print('\nLocal:')
        ewm.show_local_branches(grep=grep)
        merged = ewm.get_merged_local_branches()
        if merged:
            SOURCE_BRANCH = ewm._get_repo_settings('SOURCE_BRANCH')
            print('\nLocal merged to origin/{}:'.format(SOURCE_BRANCH))
            for branch in merged:
                print('- {}'.format(branch))


if __name__ == '__main__':
    main()
