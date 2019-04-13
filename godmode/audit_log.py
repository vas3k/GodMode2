from sqlalchemy.exc import SQLAlchemyError

from godmode.database.godmode import LogTable, GodModeDatabase


def audit_log(user, model, ids=None, action=None, details=None, reason=None):
    if not user or not model.enable_log:
        return None

    item = LogTable(
        user=user.login,
        model=str(model.name)[:64],
        action=str(action)[:512],
        ids=str(ids)[:512],
        details=str(details)[:512],
        reason=reason
    )
    GodModeDatabase.session.add(item)

    try:
        GodModeDatabase.session.commit()
    except SQLAlchemyError:
        GodModeDatabase.session.rollback()
        raise

    return item
